from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import (
    login_required as django_login_required
)
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.db.models import Sum
from .models import (
    Cliente, Pago, PagoDetalle, SerieCorrelativo, ClientePlan, OrdenTecnica,
    SerieCorrelativoLibre, DeudaExcluida, CompanySettings
)
from .utils import calcular_meses_deuda, registrar_movimiento
from .permissions import can_cobrar, can_view_deuda
import json
from datetime import datetime
import logging
from decimal import Decimal, InvalidOperation
from xhtml2pdf import pisa

logger = logging.getLogger(__name__)


def login_required(*args, **kwargs):
    kwargs['login_url'] = 'login'
    return django_login_required(*args, **kwargs)


def _to_decimal(value):
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return Decimal('0')


def _formatear_numero(serie, numero):
    return f"{serie}-{str(numero).zfill(8)}"


def _proximo_correlativo(correlativo):
    libre = (
        correlativo.libres.order_by('numero')
        .values_list('numero', flat=True)
        .first()
    )
    if libre:
        return _formatear_numero(correlativo.serie, libre)
    return _formatear_numero(correlativo.serie, correlativo.ultimo_numero + 1)


def _reservar_correlativo(correlativo):
    libre = (
        SerieCorrelativoLibre.objects
        .select_for_update()
        .filter(serie_correlativo=correlativo)
        .order_by('numero')
        .first()
    )
    if libre:
        numero = libre.numero
        libre.delete()
        return _formatear_numero(correlativo.serie, numero)
    correlativo.ultimo_numero += 1
    correlativo.save(update_fields=['ultimo_numero'])
    return _formatear_numero(correlativo.serie, correlativo.ultimo_numero)


@login_required(login_url='admin:login')
def api_get_deuda(request, cliente_id):
    if not can_view_deuda(request.user):
        return JsonResponse(
            {'items': [], 'correlativos': {}, 'planes': []},
            status=403
        )
    cliente = get_object_or_404(Cliente, id=cliente_id)
    deuda = calcular_meses_deuda(cliente)
    # Formatear para JS (plan_id es el id de ClientePlan u OT)
    items = []
    for d in deuda:
        items.append({
            'plan_id': d['id'],
            'plan_nombre': d['plan_nombre'],
            'mes_iso': d['mes'].isoformat() if d['mes'] else '',
            'mes_nombre': d['mes_nombre'],
            'monto': float(_to_decimal(d['saldo'])),
            'monto_original': float(_to_decimal(d['monto_original'])),
            'tipo': d.get('tipo', 'plan').upper(),
            'pagado': float(_to_decimal(d.get('pagado', 0)))
        })
    
    # Obtener correlativos actuales
    correlativos = {}
    for c in SerieCorrelativo.objects.all():
        correlativos[c.tipo] = _proximo_correlativo(c)

    planes = []
    for cp in cliente.planes.select_related('plan__servicio').all():
        if cp.plan and cp.plan.precio and cp.plan.precio > 0:
            nombre = cp.plan.nombre
            if cp.plan.servicio:
                nombre = f"{nombre} ({cp.plan.servicio.nombre})"
            planes.append({
                'id': cp.id,
                'nombre': nombre,
                'precio': float(_to_decimal(cp.plan.precio))
            })

    return JsonResponse({
        'items': items,
        'correlativos': correlativos,
        'planes': planes
    })


@login_required(login_url='admin:login')
def procesar_pago(request):
    if request.method != 'POST':
        return JsonResponse(
            {'status': 'error', 'message': 'Método no permitido'},
            status=405
        )
    if not can_cobrar(request.user):
        return JsonResponse(
            {'status': 'error', 'message': 'Acceso no autorizado'},
            status=403
        )
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {'status': 'error', 'message': 'Datos inválidos'},
            status=400
        )
    cliente_id = data.get('cliente_id')
    if not cliente_id:
        return JsonResponse(
            {'status': 'error', 'message': 'Falta cliente_id'},
            status=400
        )
    cliente = get_object_or_404(Cliente, id=cliente_id)
    tipo_comp = (data.get('tipo_comprobante', 'RECIBO') or 'RECIBO').upper()
    items_pagados = data.get('items_pagados', [])
    items_exonerados = data.get('items_exonerados', [])
    if not items_pagados and not items_exonerados:
        return JsonResponse(
            {
                'status': 'error',
                'message': 'No hay ítems para registrar'
            },
            status=400
        )
    try:
        with transaction.atomic():
            pago = None
            numero_comp = None
            if items_pagados:
                correlativo_obj = (
                    SerieCorrelativo.objects
                    .select_for_update()
                    .get(tipo=tipo_comp)
                )
                numero_comp = _reservar_correlativo(correlativo_obj)
                resumen = data.get('resumen_detalles', '')
                monto_total = _to_decimal(data.get('monto_total', 0))
                pago = Pago.objects.create(
                    cliente=cliente,
                    monto=monto_total,
                    tipo_comprobante=tipo_comp.capitalize(),
                    serie_numero=numero_comp,
                    detalles=resumen or 'Pago registrado'
                )

            for item in items_pagados:
                plan_id = item.get('plan_id')
                tipo_item = (item.get('tipo') or 'plan').upper()
                monto_pagar = _to_decimal(item.get('monto_pagar', 0))
                nota = item.get('nota', '')
                if tipo_item == 'OT' and plan_id and pago:
                    try:
                        ot = OrdenTecnica.objects.get(
                            id=plan_id, cliente=cliente
                        )
                    except OrdenTecnica.DoesNotExist:
                        continue
                    PagoDetalle.objects.create(
                        pago=pago,
                        ot_asociada=ot,
                        monto_parcial=monto_pagar,
                        descripcion=nota or f"Pago de OT: {ot.concepto.nombre}"
                    )
                    pagado_ot = PagoDetalle.objects.filter(
                        ot_asociada=ot
                    ).aggregate(total=Sum('monto_parcial'))['total'] or 0
                    if pagado_ot >= ot.monto:
                        ot.pagada = True
                        ot.save(update_fields=['pagada'])
                elif plan_id and pago:
                    try:
                        plan = ClientePlan.objects.get(
                            id=plan_id, cliente=cliente
                        )
                    except ClientePlan.DoesNotExist:
                        continue
                    periodo = item.get('mes_iso')
                    periodo_date = None
                    if periodo:
                        try:
                            periodo_date = datetime.strptime(
                                periodo[:10], '%Y-%m-%d'
                            ).date()
                        except (ValueError, TypeError):
                            pass
                    PagoDetalle.objects.create(
                        pago=pago,
                        plan_asociado=plan,
                        periodo_mes=periodo_date,
                        monto_parcial=monto_pagar,
                        descripcion=nota or 'Pago de mes'
                    )

            for item in items_exonerados:
                plan_id = item.get('plan_id')
                tipo_item = (item.get('tipo') or 'plan').upper()
                nota = item.get('nota') or 'Exonerado'
                if tipo_item == 'OT' and plan_id:
                    ot = OrdenTecnica.objects.filter(
                        id=plan_id, cliente=cliente
                    ).first()
                    if ot:
                        DeudaExcluida.objects.get_or_create(
                            cliente=cliente,
                            ot_asociada=ot,
                            defaults={'motivo': nota}
                        )
                        ot.exonerada = True
                        ot.pagada = False
                        ot.save(update_fields=['exonerada', 'pagada'])
                        registrar_movimiento(
                            cliente,
                            'OT exonerada',
                            f"{ot.concepto.nombre}",
                            icono='fa-ban',
                            clase='warning'
                        )
                elif plan_id:
                    plan = ClientePlan.objects.filter(
                        id=plan_id, cliente=cliente
                    ).first()
                    periodo = item.get('mes_iso')
                    if plan and periodo:
                        try:
                            periodo_date = datetime.strptime(
                                periodo[:10], '%Y-%m-%d'
                            ).date()
                        except (ValueError, TypeError):
                            periodo_date = None
                        if periodo_date:
                            DeudaExcluida.objects.get_or_create(
                                cliente=cliente,
                                plan_asociado=plan,
                                periodo_mes=periodo_date,
                                defaults={'motivo': nota}
                            )
                            registrar_movimiento(
                                cliente,
                                'Pago exonerado',
                                (
                                    f"{plan.plan.nombre} "
                                    f"{periodo_date.strftime('%m/%Y')}"
                                ),
                                icono='fa-ban',
                                clase='warning'
                            )

            if pago:
                registrar_movimiento(
                    cliente,
                    'Pago registrado',
                    (
                        f"{pago.tipo_comprobante} {pago.serie_numero}"
                        f" - S/ {pago.monto}"
                    ),
                    icono='fa-money-bill-wave',
                    clase='primary'
                )
    except SerieCorrelativo.DoesNotExist:
        return JsonResponse(
            {
                'status': 'error',
                'message': (
                    f"Serie {tipo_comp} no configurada. "
                    "Configure en Ajustes > Comprobantes."
                )
            },
            status=400
        )
    except Exception:
        logger.exception("Error al procesar pago para cliente %s", cliente_id)
        return JsonResponse(
            {
                'status': 'error',
                'message': 'Error interno al procesar el pago'
            },
            status=500
        )

    if pago:
        return JsonResponse(
            {'status': 'success', 'pago_id': pago.id, 'numero': numero_comp}
        )
    return JsonResponse({'status': 'success', 'exonerado_only': True})


@login_required(login_url='admin:login')
@require_http_methods(["POST"])
def pago_eliminar(request, pago_id):
    pago = get_object_or_404(Pago, id=pago_id)
    cliente = pago.cliente
    serie_numero = pago.serie_numero
    tipo = (pago.tipo_comprobante or '').upper()

    try:
        serie, numero_str = serie_numero.split('-', 1)
        numero = int(numero_str)
    except (ValueError, AttributeError):
        serie = None
        numero = None

    with transaction.atomic():
        if serie and numero is not None:
            correlativo = SerieCorrelativo.objects.filter(
                tipo=tipo, serie=serie
            ).first()
            if correlativo:
                SerieCorrelativoLibre.objects.get_or_create(
                    serie_correlativo=correlativo,
                    numero=numero
                )

        for item in pago.items.select_related('ot_asociada'):
            if item.ot_asociada_id:
                item.ot_asociada.pagada = False
                item.ot_asociada.save(update_fields=['pagada'])

        registrar_movimiento(
            cliente,
            'Pago eliminado',
            (
                f"{pago.tipo_comprobante} {pago.serie_numero}"
                f" - S/ {pago.monto}"
            ),
            icono='fa-trash-alt',
            clase='danger'
        )
        pago.delete()

    return redirect('cliente-detalle', pk=cliente.pk)


def _build_comprobante_context(pago, format_key='a5'):
    company_settings = CompanySettings.get_settings()
    logo_path = None
    if company_settings.logo:
        try:
            logo_path = company_settings.logo.path
        except (ValueError, OSError):
            logo_path = None
    if logo_path:
        try:
            from pathlib import Path
            logo_path = Path(logo_path).as_uri()
        except Exception:
            logo_path = None

    serie = None
    numero = pago.serie_numero
    if pago.serie_numero and '-' in pago.serie_numero:
        serie, numero = pago.serie_numero.split('-', 1)

    detalles = pago.detalles or ''
    if not detalles:
        detalles = ', '.join(
            item.descripcion for item in pago.items.all()
        )

    fmt = (format_key or 'a5').lower()
    if fmt in ('a4',):
        page_size = 'A4'
        page_margin = '12mm'
        content_width = '180mm'
        font_base = '10pt'
    elif fmt in ('carta', 'letter'):
        page_size = 'Letter'
        page_margin = '12mm'
        content_width = '180mm'
        font_base = '10pt'
    elif fmt in ('80mm', 'ticket80', 'termico80'):
        page_size = '80mm auto'
        page_margin = '4mm'
        content_width = '72mm'
        font_base = '9pt'
    elif fmt in ('58mm', 'ticket58', 'termico58'):
        page_size = '58mm auto'
        page_margin = '4mm'
        content_width = '52mm'
        font_base = '8pt'
    else:
        page_size = 'A5'
        page_margin = '12mm'
        content_width = '160mm'
        font_base = '10pt'

    return {
        'pago': pago,
        'company_settings': company_settings,
        'logo_path': logo_path,
        'serie': serie or '',
        'numero': numero or '',
        'detalles_comp': detalles or 'Pago registrado',
        'payment_method': 'Efectivo',
        'format_key': fmt,
        'page_size': page_size,
        'page_margin': page_margin,
        'content_width': content_width,
        'font_base': font_base,
        'is_ticket': fmt in ('80mm', 'ticket80', 'termico80', '58mm', 'ticket58', 'termico58'),
        'color_main': '#111827',
        'color_muted': '#6b7280',
        'color_line': '#e5e7eb',
        'color_panel': '#f9fafb'
    }


@login_required(login_url='admin:login')
def generar_pdf_pago(request, pago_id):
    pago = get_object_or_404(Pago, id=pago_id)
    template_path = 'billing_app/pdf/comprobante.html'
    formato = (request.GET.get('formato') or 'a5').lower()
    if formato not in ('a5', 'a4', 'carta', 'letter'):
        formato = 'a5'
    context = _build_comprobante_context(pago, format_key=formato)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        f'inline; filename="comp_{pago.serie_numero}.pdf"'
    )
    
    html = render_to_string(template_path, context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('Error al generar PDF', status=500)
    return response


@login_required(login_url='admin:login')
def generar_ticket_pago(request, pago_id):
    pago = get_object_or_404(Pago, id=pago_id)
    formato = (request.GET.get('formato') or '80mm').lower()
    if formato not in ('80mm', '58mm'):
        formato = '80mm'
    context = _build_comprobante_context(pago, format_key=formato)
    return render(request, 'billing_app/pdf/comprobante.html', context)
