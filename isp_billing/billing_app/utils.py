import logging
import calendar
from decimal import Decimal, ROUND_HALF_UP
from django.utils import timezone
from .models import DeudaExcluida, MovimientoHistorial, PagoDetalle
from django.db.models import Sum

logger = logging.getLogger(__name__)

MESES_ES = [
    '', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
]


def calcular_meses_deuda(cliente):
    """
    Calcula los meses de deuda para un cliente basándose en sus planes activos.
    
    Args:
        cliente: Instancia de Cliente
        
    Returns:
        list: Lista de dicts con estructura:
            - id: ID del plan o OT
            - plan_nombre: Nombre del plan u OT
            - mes: Fecha del primer día del mes (None para OT)
            - mes_nombre: Representación legible del período
            - monto_original: Monto del plan o OT
            - pagado: Monto ya pagado
            - saldo: Deuda pendiente
            - tipo: 'plan' o 'OT' (default: 'plan')
    
    Raises:
        ValueError: Si hay problemas con los datos del cliente
    """
    try:
        hoy = timezone.now().date()
        periodos_deuda = []
        
        # Exclusiones registradas
        exclusiones_plan = set(
            DeudaExcluida.objects.filter(
                cliente=cliente,
                plan_asociado__isnull=False,
                periodo_mes__isnull=False
            ).values_list('plan_asociado_id', 'periodo_mes')
        )
        exclusiones_ot = set(
            DeudaExcluida.objects.filter(
                cliente=cliente,
                ot_asociada__isnull=False
            ).values_list('ot_asociada_id', flat=True)
        )

        # Procesamos planes activos del cliente
        planes = cliente.planes.select_related('plan').all()
        for cp in planes:
            fecha_eval = cp.fecha_inicio
            if not fecha_eval:
                logger.warning(
                    "Cliente %s tiene plan %s sin fecha_inicio",
                    cliente.id,
                    cp.id
                )
                continue
            # Cobranza inicia en el mismo mes de la fecha de instalacion
            fecha_eval = fecha_eval.replace(day=1)
            if fecha_eval > hoy:
                continue
            
            # Iteramos mes a mes desde la fecha de inicio hasta hoy
            max_iter = 600
            iter_count = 0
            while fecha_eval <= hoy:
                iter_count += 1
                if iter_count > max_iter:
                    logger.error(
                        "Loop demasiado largo al calcular deuda para plan %s",
                        cp.id
                    )
                    break
                mes_inicio = fecha_eval.replace(day=1)

                if (cp.id, mes_inicio) in exclusiones_plan:
                    continue

                # Verificamos pagos registrados para este mes
                try:
                    pagado = PagoDetalle.objects.filter(
                        plan_asociado=cp,
                        periodo_mes=mes_inicio
                    ).aggregate(total=Sum('monto_parcial'))['total'] or 0
                except Exception as e:
                    logger.warning(
                        f"Error al calcular pagos para plan {cp.id}: {e}"
                    )
                    pagado = 0
                monto_mes = Decimal(str(cp.plan.precio))
                if (
                    cp.fecha_inicio
                    and mes_inicio.year == cp.fecha_inicio.year
                    and mes_inicio.month == cp.fecha_inicio.month
                    and cp.fecha_inicio.day > 1
                ):
                    dias_mes = calendar.monthrange(
                        mes_inicio.year, mes_inicio.month
                    )[1]
                    dias_restantes = dias_mes - cp.fecha_inicio.day + 1
                    if dias_restantes > 0:
                        monto_mes = (
                            monto_mes * Decimal(dias_restantes)
                            / Decimal(dias_mes)
                        ).quantize(
                            Decimal('0.01'), rounding=ROUND_HALF_UP
                        )

                pagado_decimal = Decimal(str(pagado or 0))

                # Solo añadimos si hay deuda real y el plan tiene monto > 0
                if monto_mes > 0 and pagado_decimal < monto_mes:
                    saldo = monto_mes - pagado_decimal
                    if saldo <= 0:
                        continue
                    mes_nombre_es = (
                        f"{MESES_ES[mes_inicio.month]} {mes_inicio.year}"
                    )
                    periodos_deuda.append({
                        'id': cp.id,
                        'plan_nombre': cp.plan.nombre,
                        'mes': mes_inicio,
                        'mes_nombre': mes_nombre_es,
                        'monto_original': monto_mes,
                        'pagado': pagado_decimal,
                        'saldo': saldo,
                        'tipo': 'plan'
                    })

                # Avanzar al siguiente mes de forma segura
                try:
                    if fecha_eval.month == 12:
                        fecha_eval = fecha_eval.replace(
                            year=fecha_eval.year + 1, month=1, day=1
                        )
                    else:
                        fecha_eval = fecha_eval.replace(
                            month=fecha_eval.month + 1, day=1
                        )
                except ValueError as e:
                    logger.error(f"Error al calcular fecha siguiente: {e}")
                    break

        # Procesamos ?rdenes t?cnicas no pagadas
        try:
            ots = cliente.ordenes_tecnicas.filter(exonerada=False)
            if exclusiones_ot:
                ots = ots.exclude(id__in=exclusiones_ot)
            for ot in ots:
                if ot.monto and ot.monto > 0:
                    pagado_ot = PagoDetalle.objects.filter(
                        ot_asociada=ot
                    ).aggregate(total=Sum('monto_parcial'))['total'] or 0
                    saldo_ot = ot.monto - pagado_ot
                    if saldo_ot <= 0:
                        continue
                    nombre_ot = f"OT: {ot.concepto.nombre}"
                    if (
                        ot.concepto.categoria == 'INSTALACION'
                        and ot.observaciones
                    ):
                        nombre_ot = ot.observaciones
                    periodos_deuda.append({
                        'id': ot.id,
                        'plan_nombre': nombre_ot,
                        'mes': None,
                        'mes_nombre': "Costo ?nico",
                        'monto_original': ot.monto,
                        'pagado': pagado_ot,
                        'saldo': saldo_ot,
                        'tipo': 'OT'
                    })
        except Exception as e:
            logger.warning(
                f"Error al procesar OTs para cliente {cliente.id}: {e}"
            )

        logger.info(
            f"Deuda calculada para cliente {cliente.id}: "
            f"{len(periodos_deuda)} periodos"
        )
        return periodos_deuda
        
    except Exception as e:
        logger.error(
            f"Error crítico al calcular deuda para cliente "
            f"{cliente.id}: {e}",
            exc_info=True
        )
        raise ValueError(
            f"No se pudo calcular la deuda del cliente: {str(e)}"
        )


def registrar_movimiento(
    cliente,
    tipo,
    detalle,
    icono='fa-info-circle',
    clase='secondary'
):
    try:
        MovimientoHistorial.objects.create(
            cliente=cliente,
            tipo=tipo,
            detalle=detalle,
            icono=icono,
            clase=clase
        )
    except Exception:
        logger.exception(
            "No se pudo registrar movimiento para cliente %s",
            cliente.pk if cliente else 'N/A'
        )

