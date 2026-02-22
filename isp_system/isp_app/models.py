"""
Models for ISP Management System 2026
Módulos: Geográfico, Infraestructura, Red Externa, Comercial, Técnico, RRHH, Finanzas
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# ==================== MODULO 01: NÚCLEO GEOGRÁFICO ====================

class Distrito(models.Model):
    """Tabla de distritos - Nivel jerárquico 1"""
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name = "Distrito"
        verbose_name_plural = "Distritos"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Sector(models.Model):
    """Tabla de sectores - Nivel jerárquico 2"""
    id = models.AutoField(primary_key=True)
    distrito = models.ForeignKey(Distrito, on_delete=models.CASCADE, related_name='sectores')
    nombre = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = "Sector"
        verbose_name_plural = "Sectores"
        unique_together = ('distrito', 'nombre')
        ordering = ['distrito', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} - {self.distrito.nombre}"


class Via(models.Model):
    """Tabla de vías: Av/Jr/Calle/Psj"""
    TIPO_VIA_CHOICES = [
        ('Avenida', 'Avenida'),
        ('Jiron', 'Jirón'),
        ('Calle', 'Calle'),
        ('Pasaje', 'Pasaje'),
        ('Carretera', 'Carretera'),
    ]
    
    id = models.AutoField(primary_key=True)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='vias')
    tipo_via = models.CharField(max_length=20, choices=TIPO_VIA_CHOICES)
    nombre = models.CharField(max_length=150)
    
    class Meta:
        verbose_name = "Vía"
        verbose_name_plural = "Vías"
        unique_together = ('sector', 'tipo_via', 'nombre')
        ordering = ['sector', 'tipo_via', 'nombre']
    
    def __str__(self):
        return f"{self.tipo_via} {self.nombre}"


# ==================== MODULO 02: INFRAESTRUCTURA CORE Y SEDES ====================

class Sede(models.Model):
    """Tabla de sedes administrativas"""
    id = models.AutoField(primary_key=True)
    via = models.ForeignKey(Via, on_delete=models.SET_NULL, null=True, blank=True, related_name='sedes')
    numero_municipal = models.CharField(max_length=10)
    nombre_sede = models.CharField(max_length=100)
    ruc = models.CharField(max_length=11, unique=True)
    razon_social = models.CharField(max_length=150)
    cert_digital_path = models.FileField(upload_to='certificados/', null=True, blank=True)
    
    class Meta:
        verbose_name = "Sede"
        verbose_name_plural = "Sedes"
        ordering = ['nombre_sede']
    
    def __str__(self):
        return self.nombre_sede


class ServidorMikrotik(models.Model):
    """Tabla de servidores Mikrotik"""
    id = models.AutoField(primary_key=True)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, related_name='servidores_mikrotik')
    ip_host = models.GenericIPAddressField()
    puerto_api = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(65535)])
    usuario = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = "Servidor Mikrotik"
        verbose_name_plural = "Servidores Mikrotik"
        unique_together = ('sede', 'ip_host')
    
    def __str__(self):
        return f"Mikrotik {self.sede.nombre_sede} - {self.ip_host}"


class EquipoOltEdfa(models.Model):
    """Tabla de equipos OLT y EDFA"""
    TIPO_EQUIPO_CHOICES = [
        ('OLT', 'OLT'),
        ('EDFA', 'EDFA'),
    ]
    
    id = models.AutoField(primary_key=True)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, related_name='equipos_olt_edfa')
    nombre = models.CharField(max_length=50)
    marca_modelo = models.CharField(max_length=100)
    ip_gestion = models.GenericIPAddressField()
    tipo_equipo = models.CharField(max_length=20, choices=TIPO_EQUIPO_CHOICES)
    puertos_pon_total = models.IntegerField(validators=[MinValueValidator(1)])
    
    class Meta:
        verbose_name = "Equipo OLT/EDFA"
        verbose_name_plural = "Equipos OLT/EDFA"
        unique_together = ('sede', 'nombre')
    
    def __str__(self):
        return f"{self.nombre} ({self.tipo_equipo})"


# ==================== MODULO 03: RED EXTERNA Y GIS ====================

class FibraTramo(models.Model):
    """Tabla de tramos de fibra"""
    HILOS_CHOICES = [(12, '12'), (24, '24'), (48, '48'), (96, '96'), (144, '144')]
    
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    hilos_totales = models.IntegerField(choices=HILOS_CHOICES)
    tipo_fibra = models.CharField(max_length=50)
    lat_inicio = models.DecimalField(max_digits=10, decimal_places=8)
    lon_inicio = models.DecimalField(max_digits=11, decimal_places=8)
    lat_fin = models.DecimalField(max_digits=10, decimal_places=8)
    lon_fin = models.DecimalField(max_digits=11, decimal_places=8)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Tramo de Fibra"
        verbose_name_plural = "Tramos de Fibra"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Mufa(models.Model):
    """Tabla de mufas de distribución"""
    TIPO_MUFA_CHOICES = [
        ('Troncal', 'Troncal'),
        ('Distribucion', 'Distribución'),
    ]
    
    id = models.AutoField(primary_key=True)
    via = models.ForeignKey(Via, on_delete=models.SET_NULL, null=True, blank=True, related_name='mufas')
    nombre = models.CharField(max_length=50, unique=True)
    tipo = models.CharField(max_length=30, choices=TIPO_MUFA_CHOICES)
    lat = models.DecimalField(max_digits=10, decimal_places=8)
    lon = models.DecimalField(max_digits=11, decimal_places=8)
    
    class Meta:
        verbose_name = "Mufa"
        verbose_name_plural = "Mufas"
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.tipo})"


class CajaNap(models.Model):
    """Tabla de cajas NAP"""
    id = models.AutoField(primary_key=True)
    mufa = models.ForeignKey(Mufa, on_delete=models.CASCADE, related_name='cajas_nap')
    via = models.ForeignKey(Via, on_delete=models.SET_NULL, null=True, blank=True, related_name='cajas_nap')
    nombre = models.CharField(max_length=50, unique=True)
    puertos_capacidad = models.IntegerField(validators=[MinValueValidator(1)])
    puertos_libres = models.IntegerField(validators=[MinValueValidator(0)])
    lat = models.DecimalField(max_digits=10, decimal_places=8)
    lon = models.DecimalField(max_digits=11, decimal_places=8)
    
    class Meta:
        verbose_name = "Caja NAP"
        verbose_name_plural = "Cajas NAP"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


# ==================== MODULO 04: COMERCIAL Y CLIENTES ====================

class PlanInternet(models.Model):
    """Tabla de planes de internet"""
    id = models.AutoField(primary_key=True)
    nombre_plan = models.CharField(max_length=50, unique=True)
    mbps = models.IntegerField(validators=[MinValueValidator(1)])
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    class Meta:
        verbose_name = "Plan Internet"
        verbose_name_plural = "Planes Internet"
        ordering = ['mbps']
    
    def __str__(self):
        return f"{self.nombre_plan} ({self.mbps} Mbps)"


class Cliente(models.Model):
    """Tabla de clientes"""
    ESTADO_CLIENTE_CHOICES = [
        ('Activo', 'Activo'),
        ('Suspendido', 'Suspendido'),
        ('Retirado', 'Retirado'),
    ]
    
    id = models.AutoField(primary_key=True)
    dni_ruc = models.CharField(max_length=15, unique=True)
    nombres_completos = models.CharField(max_length=200)
    via = models.ForeignKey(Via, on_delete=models.SET_NULL, null=True, blank=True, related_name='clientes')
    numero_casa = models.CharField(max_length=10)
    mz_lote_int = models.CharField(max_length=50, null=True, blank=True)
    telf = models.CharField(max_length=20)
    estado_cliente = models.CharField(max_length=20, choices=ESTADO_CLIENTE_CHOICES, default='Activo')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nombres_completos']
    
    def __str__(self):
        return f"{self.nombres_completos} ({self.dni_ruc})"


# ==================== MODULO 05: REPORTE DE INSTALACIÓN Y SERVICIO ====================

class MaterialCatalogo(models.Model):
    """Tabla de catálogo de materiales"""
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    marca = models.CharField(max_length=50)
    es_seriado = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Material Catálogo"
        verbose_name_plural = "Materiales Catálogo"
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.marca})"


class ItemSeriado(models.Model):
    """Tabla de items seriados"""
    ESTADO_CHOICES = [
        ('Almacen', 'Almacén'),
        ('Instalado', 'Instalado'),
        ('Taller', 'Taller'),
    ]
    
    id = models.AutoField(primary_key=True)
    material = models.ForeignKey(MaterialCatalogo, on_delete=models.CASCADE, related_name='items_seriados')
    nro_serie = models.CharField(max_length=100, unique=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Almacen')
    
    class Meta:
        verbose_name = "Item Seriado"
        verbose_name_plural = "Items Seriados"
    
    def __str__(self):
        return f"{self.nro_serie} - {self.material.nombre}"


class Personal(models.Model):
    """Tabla de personal"""
    ROL_CHOICES = [
        ('Tecnico', 'Técnico'),
        ('Admin', 'Administrador'),
        ('Soporte', 'Soporte'),
    ]
    
    id = models.AutoField(primary_key=True)
    sede = models.ForeignKey(Sede, on_delete=models.SET_NULL, null=True, blank=True, related_name='personal')
    nombres_apellidos = models.CharField(max_length=200)
    dni = models.CharField(max_length=15, unique=True)
    rol = models.CharField(max_length=30, choices=ROL_CHOICES)
    
    class Meta:
        verbose_name = "Personal"
        verbose_name_plural = "Personal"
        ordering = ['nombres_apellidos']
    
    def __str__(self):
        return f"{self.nombres_apellidos} ({self.rol})"


class ServicioActivo(models.Model):
    """Tabla de servicios activos"""
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='servicios_activos')
    plan = models.ForeignKey(PlanInternet, on_delete=models.SET_NULL, null=True, blank=True)
    tecnico = models.ForeignKey(Personal, on_delete=models.SET_NULL, null=True, blank=True, related_name='servicios_instalados')
    via_real_instalacion = models.ForeignKey(Via, on_delete=models.SET_NULL, null=True, blank=True, related_name='servicios_instalados')
    nap = models.ForeignKey(CajaNap, on_delete=models.SET_NULL, null=True, blank=True, related_name='servicios')
    puerto_nap_nro = models.IntegerField()
    onu_serie = models.ForeignKey(ItemSeriado, on_delete=models.SET_NULL, null=True, blank=True, related_name='servicios')
    potencia_dbm = models.DecimalField(max_digits=5, decimal_places=2)
    lat_instalacion = models.DecimalField(max_digits=10, decimal_places=8)
    lon_instalacion = models.DecimalField(max_digits=11, decimal_places=8)
    fecha_alta = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Servicio Activo"
        verbose_name_plural = "Servicios Activos"
        ordering = ['-fecha_alta']
    
    def __str__(self):
        plan_nombre = self.plan.nombre_plan if self.plan else "Sin plan"
        return f"Servicio {self.cliente.nombres_completos} - {plan_nombre}"


# ==================== MODULO 06: RRHH, LOGÍSTICA Y FLOTA ====================

class PersonalSaludDotacion(models.Model):
    """Tabla de salud y dotación del personal"""
    GRUPO_SANGUINEO_CHOICES = [
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    ]
    
    id = models.AutoField(primary_key=True)
    personal = models.OneToOneField(Personal, on_delete=models.CASCADE, related_name='salud_dotacion')
    g_sanguineo = models.CharField(max_length=5, choices=GRUPO_SANGUINEO_CHOICES)
    sctr_nro = models.CharField(max_length=50)
    talla_polo_calzado = models.CharField(max_length=20)
    
    class Meta:
        verbose_name = "Salud y Dotación Personal"
        verbose_name_plural = "Salud y Dotación Personal"
    
    def __str__(self):
        return f"Salud: {self.personal.nombres_apellidos}"


class Vehiculo(models.Model):
    """Tabla de vehículos de flota"""
    id = models.AutoField(primary_key=True)
    placa = models.CharField(max_length=15, unique=True)
    km_actual = models.IntegerField(validators=[MinValueValidator(0)])
    soat_vence = models.DateField()
    
    class Meta:
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"
        ordering = ['placa']
    
    def __str__(self):
        return self.placa


# ==================== MODULO 07: FINANZAS Y AUDITORÍA ====================

class Pago(models.Model):
    """Tabla de pagos"""
    METODO_CHOICES = [
        ('Efectivo', 'Efectivo'),
        ('Transferencia', 'Transferencia'),
        ('Tarjeta', 'Tarjeta'),
        ('Cheque', 'Cheque'),
    ]
    
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pagos')
    monto = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    fecha = models.DateTimeField(auto_now_add=True)
    metodo = models.CharField(max_length=30, choices=METODO_CHOICES)
    referencia = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        ordering = ['-fecha']
    
    def __str__(self):
        return f"Pago {self.cliente.nombres_completos} - S/.{self.monto}"


class LogAuditoria(models.Model):
    """Tabla de logs de auditoría"""
    ACCION_CHOICES = [
        ('INSERT', 'Inserción'),
        ('UPDATE', 'Actualización'),
        ('DELETE', 'Eliminación'),
    ]
    
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Personal, on_delete=models.SET_NULL, null=True, blank=True, related_name='logs_auditoria')
    accion = models.CharField(max_length=10, choices=ACCION_CHOICES)
    tabla_afectada = models.CharField(max_length=50)
    valor_anterior = models.TextField(null=True, blank=True)
    valor_nuevo = models.TextField(null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Log Auditoría"
        verbose_name_plural = "Logs Auditoría"
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.accion} - {self.tabla_afectada} ({self.fecha})"
