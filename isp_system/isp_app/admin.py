"""
Admin configuration for ISP Management System
"""
from django.contrib import admin
from .models import (
    Distrito, Sector, Via, Sede, ServidorMikrotik, EquipoOltEdfa,
    FibraTramo, Mufa, CajaNap, PlanInternet, Cliente,
    MaterialCatalogo, ItemSeriado, Personal, ServicioActivo,
    PersonalSaludDotacion, Vehiculo, Pago, LogAuditoria
)

# ==================== MODULO 01: GEOGRÁFICO ====================

@admin.register(Distrito)
class DistritoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'distrito')
    list_filter = ('distrito',)
    search_fields = ('nombre',)


@admin.register(Via)
class ViaAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo_via', 'nombre', 'sector')
    list_filter = ('tipo_via', 'sector')
    search_fields = ('nombre',)


# ==================== MODULO 02: INFRAESTRUCTURA ====================

@admin.register(Sede)
class SedeAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_sede', 'ruc', 'numero_municipal')
    search_fields = ('nombre_sede', 'ruc', 'razon_social')


@admin.register(ServidorMikrotik)
class ServidorMikrotikAdmin(admin.ModelAdmin):
    list_display = ('id', 'sede', 'ip_host', 'puerto_api', 'usuario')
    list_filter = ('sede',)
    search_fields = ('ip_host', 'usuario')


@admin.register(EquipoOltEdfa)
class EquipoOltEdfaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'tipo_equipo', 'sede', 'ip_gestion')
    list_filter = ('tipo_equipo', 'sede')
    search_fields = ('nombre', 'marca_modelo')


# ==================== MODULO 03: RED EXTERNA ====================

@admin.register(FibraTramo)
class FibraTramoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'hilos_totales', 'tipo_fibra')
    list_filter = ('hilos_totales', 'tipo_fibra')
    search_fields = ('nombre',)


@admin.register(Mufa)
class MufaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'tipo', 'via', 'lat', 'lon')
    list_filter = ('tipo',)
    search_fields = ('nombre',)


@admin.register(CajaNap)
class CajaNapAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'mufa', 'puertos_capacidad', 'puertos_libres')
    list_filter = ('mufa',)
    search_fields = ('nombre',)


# ==================== MODULO 04: COMERCIAL ====================

@admin.register(PlanInternet)
class PlanInternetAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_plan', 'mbps', 'precio')
    list_filter = ('mbps',)
    search_fields = ('nombre_plan',)


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombres_completos', 'dni_ruc', 'estado_cliente', 'telf')
    list_filter = ('estado_cliente', 'via')
    search_fields = ('nombres_completos', 'dni_ruc')


# ==================== MODULO 05: SERVICIO TÉCNICO ====================

@admin.register(MaterialCatalogo)
class MaterialCatalogoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'marca', 'es_seriado')
    list_filter = ('es_seriado', 'marca')
    search_fields = ('nombre',)


@admin.register(ItemSeriado)
class ItemSeriadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nro_serie', 'material', 'estado')
    list_filter = ('estado', 'material')
    search_fields = ('nro_serie',)


@admin.register(Personal)
class PersonalAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombres_apellidos', 'dni', 'rol', 'sede')
    list_filter = ('rol', 'sede')
    search_fields = ('nombres_apellidos', 'dni')


@admin.register(ServicioActivo)
class ServicioActivoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'plan', 'tecnico', 'nap', 'fecha_alta')
    list_filter = ('plan', 'nap', 'fecha_alta')
    search_fields = ('cliente__nombres_completos',)


# ==================== MODULO 06: RRHH ====================

@admin.register(PersonalSaludDotacion)
class PersonalSaludDotacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'personal', 'g_sanguineo', 'sctr_nro')
    list_filter = ('g_sanguineo',)
    search_fields = ('personal__nombres_apellidos',)


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('id', 'placa', 'km_actual', 'soat_vence')
    list_filter = ('soat_vence',)
    search_fields = ('placa',)


# ==================== MODULO 07: FINANZAS ====================

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'monto', 'metodo', 'fecha')
    list_filter = ('metodo', 'fecha')
    search_fields = ('cliente__nombres_completos',)


@admin.register(LogAuditoria)
class LogAuditoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'accion', 'tabla_afectada', 'fecha')
    list_filter = ('accion', 'tabla_afectada', 'fecha')
    search_fields = ('tabla_afectada',)
    readonly_fields = ('usuario', 'accion', 'tabla_afectada', 'valor_anterior', 'valor_nuevo', 'fecha')
