from django.db import models
from decimal import Decimal
from typing import Any, cast
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings


# ===== GEOGRÁFICO =====

class Distrito(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class Sector(models.Model):
    distrito = models.ForeignKey(
        Distrito, on_delete=models.CASCADE, related_name='sectores'
    )
    nombre = models.CharField(max_length=100)

    class Meta:
        unique_together = ('distrito', 'nombre')

    def __str__(self):
        return f"{self.nombre} ({self.distrito.nombre})"


class Via(models.Model):
    TIPO_CHOICES = [
        ('AVENIDA', 'Avenida'),
        ('JIRON', 'Jirón'),
        ('CALLE', 'Calle'),
        ('PASAJE', 'Pasaje'),
    ]
    sector = models.ForeignKey(
        Sector, on_delete=models.CASCADE, related_name='vias'
    )
    tipo = models.CharField(
        max_length=15, choices=TIPO_CHOICES, default='CALLE'
    )
    nombre = models.CharField(max_length=150)

    def __str__(self):
        return f"{cast(Any, self).get_tipo_display()} {self.nombre}"


# ===== SERVICIOS, PLANES, OT =====

class Servicio(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class Plan(models.Model):
    servicio = models.ForeignKey(
        Servicio, on_delete=models.CASCADE, related_name='planes',
        null=True, blank=True
    )
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        servicio_nombre = (
            self.servicio.nombre if self.servicio else "Sin servicio"
        )
        return f"{servicio_nombre} - {self.nombre} (S/ {self.precio})"


class OrdenTecnicaConcepto(models.Model):
    CAT_CHOICES = [
        ('INSTALACION', 'Instalación'),
        ('AVERIAS', 'Averías'),
        ('CORTES', 'Cortes'),
        ('RECONEXION', 'Reconexión'),
    ]
    categoria = models.CharField(
        max_length=20, choices=CAT_CHOICES, default='AVERIAS'
    )
    nombre = models.CharField(max_length=150)
    precio_sugerido = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('0')
    )

    def __str__(self):
        return f"[{cast(Any, self).get_categoria_display()}] {self.nombre}"


class Tecnico(models.Model):
    nombre = models.CharField(max_length=100)
    dni = models.CharField(max_length=8, unique=True)
    celular = models.CharField(max_length=9)
    activo = models.BooleanField(
        default=True,
        help_text='Indica si el plan está activo para el cliente'
    )

    def __str__(self):
        return self.nombre


# ===== CLIENTE =====

class Cliente(models.Model):
    CONEXION_CHOICES = [
        ('PPPOE', 'PPPoE'),
        ('DHCP', 'DHCP'),
        ('STATIC', 'Estática'),
    ]
    apellidos = models.CharField(max_length=100)
    nombres = models.CharField(max_length=100)
    dni = models.CharField(
        max_length=8,
        validators=[
            RegexValidator(r'^\d{8}$', 'DNI debe ser de 8 dígitos')
        ],
        unique=True
    )
    celular = models.CharField(
        max_length=9,
        validators=[
            RegexValidator(r'^\d{9}$', 'Celular debe ser de 9 dígitos')
        ]
    )
    via = models.ForeignKey(
        Via, on_delete=models.PROTECT, related_name='clientes'
    )
    referencia = models.TextField(
        blank=True, null=True,
        help_text="Numeración o referencia de ubicación"
    )
    fecha_instalacion = models.DateField(
        null=True, blank=True,
        help_text="Fecha de instalacion del servicio"
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)

    # Campos Técnicos
    estado_activo = models.BooleanField(default=True)
    tipo_conexion = models.CharField(
        max_length=10, choices=CONEXION_CHOICES, default='PPPOE'
    )
    usuario_pppoe = models.CharField(max_length=50, blank=True, null=True)
    password_pppoe = models.CharField(
        max_length=128, blank=True, null=True
    )  # Almacena hash
    ip_asignada = models.GenericIPAddressField(blank=True, null=True)
    mikrotik_vinculado = models.ForeignKey(
        'MikrotikConfig', on_delete=models.SET_NULL,
        null=True, blank=True
    )

    def set_pppoe_password(self, raw_password: str):
        """Encripta y almacena la contraseña PPPoE"""
        if raw_password:
            self.password_pppoe = make_password(raw_password)

    def check_pppoe_password(self, raw_password: str) -> bool:
        """Verifica la contraseña PPPoE contra el hash almacenado"""
        if not self.password_pppoe:
            return False
        return check_password(raw_password, self.password_pppoe)

    def __str__(self):
        return f"{self.apellidos}, {self.nombres}"


# --- Mikrotik & Red ---

class MikrotikConfig(models.Model):
    nombre = models.CharField(max_length=100)
    ip_host = models.CharField(max_length=100)
    usuario = models.CharField(max_length=50)
    password = models.CharField(max_length=128)  # Hash de contraseña
    puerto_api = models.IntegerField(default=8728)
    activo = models.BooleanField(default=True)

    def set_password(self, raw_password: str):
        """Encripta y almacena la contraseña"""
        self.password = make_password(raw_password)

    def check_password(self, raw_password: str) -> bool:
        """Verifica la contraseña contra el hash almacenado"""
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.nombre} ({self.ip_host})"


class IPPool(models.Model):
    mikrotik = models.ForeignKey(
        MikrotikConfig, on_delete=models.CASCADE, related_name='pools'
    )
    nombre = models.CharField(max_length=100)
    rango = models.CharField(
        max_length=100,
        help_text="Ej: 192.168.10.2-192.168.10.254"
    )

    def __str__(self):
        return f"{self.nombre} - {self.mikrotik.nombre}"


class IPStaticaDisponible(models.Model):
    mikrotik = models.ForeignKey(
        MikrotikConfig, on_delete=models.CASCADE
    )
    ip = models.GenericIPAddressField()
    en_uso = models.BooleanField(default=False)

    def __str__(self):
        return str(self.ip)


# --- Planes y Cobranza ---

class ClientePlan(models.Model):
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, related_name='planes'
    )
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_cobranza = models.IntegerField(
        help_text="Día del mes para cobrar (1-31)"
    )
    activo = models.BooleanField(default=True)
    activo = models.BooleanField(
        default=False,
        help_text="Indica si el plan está activo para el cliente"
    )

    def __str__(self):
        return f"{self.cliente} - {self.plan}"


# --- Billing ---

class EgresoConcepto(models.Model):
    nombre = models.CharField(max_length=120, unique=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Egreso(models.Model):
    TIPO_CHOICES = [
        ('RECIBO', 'Recibo'),
        ('BOLETA', 'Boleta'),
        ('FACTURA', 'Factura'),
        ('OTRO', 'Otro')
    ]
    fecha = models.DateField()
    tipo_comprobante = models.CharField(
        max_length=20, choices=TIPO_CHOICES, default='RECIBO'
    )
    numero_comprobante = models.CharField(max_length=30, blank=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    concepto = models.ForeignKey(
        EgresoConcepto, on_delete=models.PROTECT, related_name='egresos'
    )
    responsable = models.CharField(max_length=120)
    observaciones = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.concepto.nombre} - S/ {self.monto}"


# --- Roles ---

class AppRole(models.Model):
    nombre = models.CharField(max_length=60, unique=True)
    can_cobrar = models.BooleanField(default=False)
    can_delete_cliente = models.BooleanField(default=False)
    can_view_deuda = models.BooleanField(default=True)
    can_manage_ots = models.BooleanField(default=True)
    can_manage_ajustes = models.BooleanField(default=False)
    can_manage_caja = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre


class UserRole(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    role = models.ForeignKey(
        AppRole, on_delete=models.PROTECT, related_name='users'
    )

    def __str__(self):
        return f"{self.user} -> {self.role}"


class CompanySettings(models.Model):
    """Configuración multi-empresa para personalización del sistema"""
    nombre_empresa = models.CharField(
        max_length=200,
        default='Nombre de la Empresa',
        verbose_name='Nombre de la Empresa'
    )
    ruc = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='RUC'
    )
    direccion_fiscal = models.TextField(
        blank=True,
        verbose_name='Dirección Fiscal'
    )
    logo = models.ImageField(
        upload_to='company_logos/',
        blank=True,
        null=True,
        verbose_name='Logo de la Empresa'
    )
    telefono = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Teléfono'
    )
    email = models.EmailField(
        blank=True,
        verbose_name='Email'
    )
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Configuración de Empresa'
        verbose_name_plural = 'Configuración de Empresa'

    def __str__(self):
        return self.nombre_empresa

    @classmethod
    def get_settings(cls):
        """Obtiene o crea la única instancia de configuración"""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings


class SerieCorrelativo(models.Model):
    TIPO_CHOICES = [
        ('BOLETA', 'Boleta'),
        ('FACTURA', 'Factura'),
        ('RECIBO', 'Recibo')
    ]
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, unique=True)
    serie = models.CharField(max_length=4)
    ultimo_numero = models.PositiveIntegerField(default=0)

    def next_number(self):
        return f"{self.serie}-{str(self.ultimo_numero + 1).zfill(8)}"

    def __str__(self):
        return f"{self.tipo} - {self.serie}"


class Pago(models.Model):
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, related_name='pagos'
    )
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    tipo_comprobante = models.CharField(
        max_length=10
    )  # Boleta, Factura, Recibo
    serie_numero = models.CharField(
        max_length=20
    )  # E.g. R001-00000001
    detalles = models.TextField(
        help_text="Detalle de meses pagados"
    )
    pdf_comprobante = models.FileField(
        upload_to='comprobantes/', null=True, blank=True
    )

    def __str__(self):
        return f"{self.serie_numero} - {self.monto}"


# --- Ordenes Técnicas ---

class OrdenTecnica(models.Model):
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE,
        related_name='ordenes_tecnicas'
    )
    concepto = models.ForeignKey(
        OrdenTecnicaConcepto, on_delete=models.PROTECT
    )
    plan_asociado = models.ForeignKey(
        'ClientePlan', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='ordenes_tecnicas'
    )
    servicio_afectado = models.ForeignKey(
        Servicio, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='ordenes_tecnicas'
    )
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    observaciones = models.TextField(blank=True, null=True)
    completada = models.BooleanField(default=False)
    pagada = models.BooleanField(default=False)
    exonerada = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_asistencia = models.DateField(
        null=True, blank=True,
        help_text="Fecha de instalación o asistencia"
    )
    fecha_finalizacion = models.DateTimeField(
        null=True, blank=True,
        help_text="Fecha y hora en que el técnico realizó/finalizó el trabajo"
    )
    tecnico_asignado = models.ForeignKey(
        Tecnico, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='ordenes'
    )

    def __str__(self):
        return (
            f"OT-{cast(Any, self).id}: {self.concepto.nombre}"
            f" - {self.cliente}"
        )


class PagoDetalle(models.Model):
    pago = models.ForeignKey(
        Pago, on_delete=models.CASCADE, related_name='items'
    )
    plan_asociado = models.ForeignKey(
        ClientePlan, on_delete=models.CASCADE, null=True, blank=True
    )
    ot_asociada = models.ForeignKey(
        OrdenTecnica, on_delete=models.CASCADE, null=True, blank=True
    )
    periodo_mes = models.DateField(
        help_text="Primer día del mes pagado", null=True, blank=True
    )
    monto_parcial = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField(
        max_length=200,
        help_text="Ej: Mes completo, 15 días, OT, etc"
    )

    def __str__(self):
        return f"Pago {cast(Any, self.pago).id} - {self.descripcion}"


class MovimientoHistorial(models.Model):
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, related_name='movimientos_historial'
    )
    fecha = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=50)
    detalle = models.TextField()
    icono = models.CharField(max_length=50, default='fa-info-circle')
    clase = models.CharField(max_length=20, default='secondary')

    def __str__(self):
        return f"{self.cliente} - {self.tipo} - {self.fecha:%Y-%m-%d %H:%M}"


class DeudaExcluida(models.Model):
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, related_name='deudas_excluidas'
    )
    plan_asociado = models.ForeignKey(
        ClientePlan, on_delete=models.CASCADE, null=True, blank=True
    )
    periodo_mes = models.DateField(null=True, blank=True)
    ot_asociada = models.ForeignKey(
        OrdenTecnica, on_delete=models.CASCADE, null=True, blank=True
    )
    motivo = models.CharField(max_length=200, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['cliente', 'plan_asociado', 'periodo_mes'],
                name='uniq_deuda_excluida_plan_periodo'
            ),
            models.UniqueConstraint(
                fields=['cliente', 'ot_asociada'],
                name='uniq_deuda_excluida_ot'
            )
        ]

    def __str__(self):
        ot_id = cast(Any, self).ot_asociada_id
        if ot_id:
            return f"Excluida OT {ot_id} - {self.cliente}"
        return (
            f"Excluida {cast(Any, self).plan_asociado_id}"
            f" {self.periodo_mes}"
            f" - {self.cliente}"
        )


class SerieCorrelativoLibre(models.Model):
    serie_correlativo = models.ForeignKey(
        SerieCorrelativo, on_delete=models.CASCADE, related_name='libres'
    )
    numero = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('serie_correlativo', 'numero')

    def __str__(self):
        return f"{self.serie_correlativo.serie}-{str(self.numero).zfill(8)}"
