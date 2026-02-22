"""
URL Configuration for ISP App
"""
from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.index, name='index'),
    
    # MODULO 01: Geográfico
    path('geografico/', views.geografico_integrado, name='geografico-integrado'),
    path('distritos/', views.DistritoListView.as_view(), name='distrito-list'),
    path('distrito/<int:pk>/', views.DistritoDetailView.as_view(), name='distrito-detail'),
    path('distrito/crear/', views.DistritoCreateView.as_view(), name='distrito-create'),
    path('distrito/<int:pk>/editar/', views.DistritoUpdateView.as_view(), name='distrito-update'),
    path('distrito/<int:pk>/eliminar/', views.DistritoDeleteView.as_view(), name='distrito-delete'),
    
    path('sectores/', views.SectorListView.as_view(), name='sector-list'),
    path('sector/crear/', views.SectorCreateView.as_view(), name='sector-create'),
    
    path('vias/', views.ViaListView.as_view(), name='via-list'),
    path('via/crear/', views.ViaCreateView.as_view(), name='via-create'),
    
    # MODULO 02: Infraestructura
    path('sedes/', views.SedeListView.as_view(), name='sede-list'),
    path('sede/<int:pk>/', views.SedeDetailView.as_view(), name='sede-detail'),
    path('sede/crear/', views.SedeCreateView.as_view(), name='sede-create'),
    path('sede/<int:pk>/editar/', views.SedeUpdateView.as_view(), name='sede-update'),
    
    # MODULO 03: Red Externa
    path('mufas/', views.MufaListView.as_view(), name='mufa-list'),
    path('cajas-nap/', views.CajaNapListView.as_view(), name='caja-nap-list'),
    path('fibra-tramos/', views.FibraTramoListView.as_view(), name='fibra-list'),
    
    # MODULO 04: Comercial
    path('clientes/', views.ClienteListView.as_view(), name='cliente-list'),
    path('cliente/<int:pk>/', views.ClienteDetailView.as_view(), name='cliente-detail'),
    path('cliente/crear/', views.ClienteCreateView.as_view(), name='cliente-create'),
    path('cliente/<int:pk>/editar/', views.ClienteUpdateView.as_view(), name='cliente-update'),
    
    path('planes/', views.PlanInternetListView.as_view(), name='plan-list'),
    path('plan/crear/', views.PlanInternetCreateView.as_view(), name='plan-create'),
    
    # MODULO 05: Servicio Técnico
    path('servicios/', views.ServicioActivoListView.as_view(), name='servicio-list'),
    path('servicio/<int:pk>/', views.ServicioActivoDetailView.as_view(), name='servicio-detail'),
    path('servicio/crear/', views.ServicioActivoCreateView.as_view(), name='servicio-create'),
    
    path('materiales/', views.MaterialListView.as_view(), name='material-list'),
    path('items-seriados/', views.ItemSeriadoListView.as_view(), name='item-list'),
    
    # MODULO 06: RRHH
    path('personal/', views.PersonalListView.as_view(), name='personal-list'),
    path('personal/<int:pk>/', views.PersonalDetailView.as_view(), name='personal-detail'),
    
    # MODULO 07: Finanzas
    path('pagos/', views.PagoListView.as_view(), name='pago-list'),
    path('pago/<int:pk>/', views.PagoDetailView.as_view(), name='pago-detail'),
    path('pago/crear/', views.PagoCreateView.as_view(), name='pago-create'),
    
    # Reportes
    path('reportes/', views.reportes_generales, name='reportes'),
]
