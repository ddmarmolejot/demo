"""
Views for ISP Management System
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum, Count
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required

from .models import (
    Distrito, Sector, Via, Sede, Cliente, PlanInternet, ServicioActivo,
    Personal, Pago, MaterialCatalogo, ItemSeriado, CajaNap, Mufa,
    FibraTramo
)
from .forms import (
    DistritoForm, SectorForm, ViaForm, SedeForm, ClienteForm,
    PlanInternetForm, ServicioActivoForm, PagoForm
)


# ==================== DASHBOARD ====================

# ==================== DASHBOARD ====================

@login_required(login_url='admin:login')
def index(request):
    """Dashboard principal del sistema"""
    clientes_activos = Cliente.objects.filter(
        estado_cliente='Activo'
    ).count()
    total_ingresos = (
        Pago.objects.aggregate(Sum('monto'))['monto__sum'] or 0
    )
    context = {
        'total_clientes': Cliente.objects.count(),
        'clientes_activos': clientes_activos,
        'total_servicios': ServicioActivo.objects.count(),
        'total_ingresos': total_ingresos,
        'total_personal': Personal.objects.count(),
        'total_sedes': Sede.objects.count(),
        'ultimos_pagos': Pago.objects.all()[:5],
        'ultimos_servicios': ServicioActivo.objects.all()[:5],
    }
    return render(request, 'isp_app/index.html', context)


# ==================== MODULO 01: GEOGRÁFICO ====================

def geografico_integrado(request):
    """Vista integrada del módulo geográfico.
    
    Distritos, Sectores y Vías en una sola página"""
    context = {
        'distritos': Distrito.objects.all(),
        'sectores': Sector.objects.all(),
        'vias': Via.objects.all(),
        'distrito_form': DistritoForm(),
        'sector_form': SectorForm(),
        'via_form': ViaForm(),
        'tab_activo': request.GET.get('tab', 'distritos'),
    }
    
    # Procesar formularios POST
    if request.method == 'POST':
        tab = request.POST.get('tab', 'distritos')
        
        if tab == 'distritos':
            form = DistritoForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Distrito creado exitosamente'
                )
                return redirect(
                    f'{reverse("geografico-integrado")}'
                    '?tab=distritos'
                )
            context['distrito_form'] = form
            context['tab_activo'] = 'distritos'

        elif tab == 'sectores':
            form = SectorForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Sector creado exitosamente')
                return redirect(
                    f'{reverse("geografico-integrado")}'
                    '?tab=sectores'
                )
            context['sector_form'] = form
            context['tab_activo'] = 'sectores'

        elif tab == 'vias':
            form = ViaForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Vía creada exitosamente')
                return redirect(
                    f'{reverse("geografico-integrado")}'
                    '?tab=vias'
                )
            context['via_form'] = form
            context['tab_activo'] = 'vias'

    return render(
        request,
        'isp_app/geografico/geografico_integrado.html',
        context
    )


class DistritoListView(ListView):
    """Lista de distritos"""
    model = Distrito
    template_name = 'isp_app/geografico/distrito_list.html'
    context_object_name = 'distritos'
    paginate_by = 20


class DistritoDetailView(DetailView):
    """Detalle de distrito con sus sectores"""
    model = Distrito
    template_name = 'isp_app/geografico/distrito_detail.html'
    context_object_name = 'distrito'


class DistritoCreateView(CreateView):
    """Crear nuevo distrito"""
    model = Distrito
    form_class = DistritoForm
    template_name = 'isp_app/geografico/distrito_form.html'
    success_url = reverse_lazy('distrito-list')


class DistritoUpdateView(UpdateView):
    """Actualizar distrito"""
    model = Distrito
    form_class = DistritoForm
    template_name = 'isp_app/geografico/distrito_form.html'
    success_url = reverse_lazy('distrito-list')


class DistritoDeleteView(DeleteView):
    """Eliminar distrito"""
    model = Distrito
    template_name = 'isp_app/geografico/distrito_confirm_delete.html'
    success_url = reverse_lazy('distrito-list')


class SectorListView(ListView):
    """Lista de sectores"""
    model = Sector
    template_name = 'isp_app/geografico/sector_list.html'
    context_object_name = 'sectores'
    paginate_by = 20


class SectorCreateView(CreateView):
    """Crear nuevo sector"""
    model = Sector
    form_class = SectorForm
    template_name = 'isp_app/geografico/sector_form.html'
    success_url = reverse_lazy('sector-list')


class ViaListView(ListView):
    """Lista de vías"""
    model = Via
    template_name = 'isp_app/geografico/via_list.html'
    context_object_name = 'vias'
    paginate_by = 20


class ViaCreateView(CreateView):
    """Crear nueva vía"""
    model = Via
    form_class = ViaForm
    template_name = 'isp_app/geografico/via_form.html'
    success_url = reverse_lazy('via-list')


# ==================== MODULO 02: INFRAESTRUCTURA ====================

class SedeListView(ListView):
    """Lista de sedes"""
    model = Sede
    template_name = 'isp_app/infraestructura/sede_list.html'
    context_object_name = 'sedes'
    paginate_by = 20


class SedeDetailView(DetailView):
    """Detalle de sede con equipos"""
    model = Sede
    template_name = 'isp_app/infraestructura/sede_detail.html'
    context_object_name = 'sede'


class SedeCreateView(CreateView):
    """Crear nueva sede"""
    model = Sede
    form_class = SedeForm
    template_name = 'isp_app/infraestructura/sede_form.html'
    success_url = reverse_lazy('sede-list')


class SedeUpdateView(UpdateView):
    """Actualizar sede"""
    model = Sede
    form_class = SedeForm
    template_name = 'isp_app/infraestructura/sede_form.html'
    success_url = reverse_lazy('sede-list')


# ==================== MODULO 03: RED EXTERNA ====================

class MufaListView(ListView):
    """Lista de mufas"""
    model = Mufa
    template_name = 'isp_app/red_externa/mufa_list.html'
    context_object_name = 'mufas'
    paginate_by = 20


class CajaNapListView(ListView):
    """Lista de cajas NAP"""
    model = CajaNap
    template_name = 'isp_app/red_externa/caja_nap_list.html'
    context_object_name = 'cajas_nap'
    paginate_by = 20


class FibraTramoListView(ListView):
    """Lista de tramos de fibra"""
    model = FibraTramo
    template_name = 'isp_app/red_externa/fibra_tramo_list.html'
    context_object_name = 'fibras'
    paginate_by = 20


# ==================== MODULO 04: COMERCIAL ====================

class ClienteListView(ListView):
    """Lista de clientes"""
    model = Cliente
    template_name = 'isp_app/comercial/cliente_list.html'
    context_object_name = 'clientes'
    paginate_by = 20

    def get_queryset(self):
        queryset = Cliente.objects.all()
        estado = self.request.GET.get('estado')
        if estado:
            queryset = queryset.filter(estado_cliente=estado)
        return queryset


class ClienteDetailView(DetailView):
    """Detalle del cliente con servicios y pagos"""
    model = Cliente
    template_name = 'isp_app/comercial/cliente_detail.html'
    context_object_name = 'cliente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente = self.get_object()
        context['servicios'] = cliente.servicios_activos.all()  # type: ignore
        context['pagos'] = cliente.pagos.all()  # type: ignore
        return context


class ClienteCreateView(CreateView):
    """Crear nuevo cliente"""
    model = Cliente
    form_class = ClienteForm
    template_name = 'isp_app/comercial/cliente_form.html'
    success_url = reverse_lazy('cliente-list')


class ClienteUpdateView(UpdateView):
    """Actualizar cliente"""
    model = Cliente
    form_class = ClienteForm
    template_name = 'isp_app/comercial/cliente_form.html'
    success_url = reverse_lazy('cliente-list')


class PlanInternetListView(ListView):
    """Lista de planes de internet"""
    model = PlanInternet
    template_name = 'isp_app/comercial/plan_list.html'
    context_object_name = 'planes'


class PlanInternetCreateView(CreateView):
    """Crear nuevo plan"""
    model = PlanInternet
    form_class = PlanInternetForm
    template_name = 'isp_app/comercial/plan_form.html'
    success_url = reverse_lazy('plan-list')


# ==================== MODULO 05: SERVICIO TÉCNICO ====================

class ServicioActivoListView(ListView):
    """Lista de servicios activos"""
    model = ServicioActivo
    template_name = 'isp_app/tecnico/servicio_list.html'
    context_object_name = 'servicios'
    paginate_by = 20


class ServicioActivoDetailView(DetailView):
    """Detalle del servicio instalado"""
    model = ServicioActivo
    template_name = 'isp_app/tecnico/servicio_detail.html'
    context_object_name = 'servicio'


class ServicioActivoCreateView(CreateView):
    """Registrar nuevo servicio"""
    model = ServicioActivo
    form_class = ServicioActivoForm
    template_name = 'isp_app/tecnico/servicio_form.html'
    success_url = reverse_lazy('servicio-list')


class MaterialListView(ListView):
    """Lista de materiales en catálogo"""
    model = MaterialCatalogo
    template_name = 'isp_app/tecnico/material_list.html'
    context_object_name = 'materiales'
    paginate_by = 20


class ItemSeriadoListView(ListView):
    """Lista de items seriados (ONUs, equipos)"""
    model = ItemSeriado
    template_name = 'isp_app/tecnico/item_seriado_list.html'
    context_object_name = 'items'
    paginate_by = 20

    def get_queryset(self):
        queryset = ItemSeriado.objects.all()
        estado = self.request.GET.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset


# ==================== MODULO 06: RRHH ====================

class PersonalListView(ListView):
    """Lista de personal"""
    model = Personal
    template_name = 'isp_app/rrhh/personal_list.html'
    context_object_name = 'personal'
    paginate_by = 20


class PersonalDetailView(DetailView):
    """Detalle del personal"""
    model = Personal
    template_name = 'isp_app/rrhh/personal_detail.html'
    context_object_name = 'persona'


# ==================== MODULO 07: FINANZAS ====================

class PagoListView(ListView):
    """Lista de pagos"""
    model = Pago
    template_name = 'isp_app/finanzas/pago_list.html'
    context_object_name = 'pagos'
    paginate_by = 20

    def get_queryset(self):
        return Pago.objects.select_related('cliente').order_by('-fecha')


class PagoDetailView(DetailView):
    """Detalle del pago"""
    model = Pago
    template_name = 'isp_app/finanzas/pago_detail.html'
    context_object_name = 'pago'


class PagoCreateView(CreateView):
    """Registrar nuevo pago"""
    model = Pago
    form_class = PagoForm
    template_name = 'isp_app/finanzas/pago_form.html'
    success_url = reverse_lazy('pago-list')


def reportes_generales(request):
    """Reporte general del sistema"""
    clientes_estado = Cliente.objects.values(
        'estado_cliente'
    ).annotate(count=Count('id'))
    servicios_plan = ServicioActivo.objects.values(
        'plan__nombre_plan'
    ).annotate(count=Count('id'))
    items_estado = ItemSeriado.objects.values(
        'estado'
    ).annotate(count=Count('id'))
    ingresos_mes = Pago.objects.extra(
        select={'mes': 'strftime("%Y-%m", fecha)'}
    ).values('mes').annotate(total=Sum('monto'))
    context = {
        'clientes_por_estado': clientes_estado,
        'servicios_por_plan': servicios_plan,
        'items_por_estado': items_estado,
        'ingresos_por_mes': ingresos_mes,
    }
    return render(request, 'isp_app/reportes/general.html', context)
