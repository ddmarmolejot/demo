# Management Commands y Scripts Útiles
# Colocar en: billing_app/management/commands/ o isp_app/management/commands/

# ========================
# encrypt_passwords.py
# ========================
# Ubicación: billing_app/management/commands/encrypt_passwords.py

"""
Management command para encriptar contraseñas almacenadas en texto plano
Uso: python manage.py encrypt_passwords
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from billing_app.models import Cliente, MikrotikConfig

class Command(BaseCommand):
    help = 'Encripta contraseñas almacenadas en texto plano'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando encriptación de contraseñas...'))
        
        # Encriptar Cliente.password_pppoe
        clientes = Cliente.objects.exclude(password_pppoe__isnull=True).exclude(password_pppoe='')
        count_clientes = 0
        for cliente in clientes:
            if not cliente.password_pppoe.startswith('pbkdf2_sha256$'):
                try:
                    cliente.set_pppoe_password(cliente.password_pppoe)
                    cliente.save()
                    count_clientes += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error en Cliente {cliente.id}: {e}'))
        
        # Encriptar MikrotikConfig.password
        configs = MikrotikConfig.objects.exclude(password__isnull=True).exclude(password='')
        count_configs = 0
        for config in configs:
            if not config.password.startswith('pbkdf2_sha256$'):
                try:
                    config.set_password(config.password)
                    config.save()
                    count_configs += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error en MikrotikConfig {config.id}: {e}'))
        
        self.stdout.write(self.style.SUCCESS(
            f'✓ Contraseñas encriptadas:\n'
            f'  - Clientes: {count_clientes}\n'
            f'  - Configuraciones Mikrotik: {count_configs}'
        ))


# ========================
# create_indexes.py
# ========================
# Ubicación: billing_app/management/commands/create_indexes.py

"""
Management command para crear índices en la base de datos
Uso: python manage.py create_indexes
"""

from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Crea índices en campos críticos para mejorar performance'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_cliente_dni ON billing_app_cliente(dni);",
                "CREATE INDEX IF NOT EXISTS idx_cliente_fecha ON billing_app_cliente(fecha_registro);",
                "CREATE INDEX IF NOT EXISTS idx_pago_cliente ON billing_app_pago(cliente_id);",
                "CREATE INDEX IF NOT EXISTS idx_pago_fecha ON billing_app_pago(fecha);",
                "CREATE INDEX IF NOT EXISTS idx_ot_cliente ON billing_app_ordentecnica(cliente_id);",
                "CREATE INDEX IF NOT EXISTS idx_ot_estado ON billing_app_ordentecnica(completada, pagada);",
            ]
            
            for index in indexes:
                try:
                    cursor.execute(index)
                    self.stdout.write(self.style.SUCCESS(f'✓ {index}'))
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'⚠ {index}: {e}'))


# ========================
# generate_report.py
# ========================
# Ubicación: billing_app/management/commands/generate_report.py

"""
Management command para generar reportes
Uso: python manage.py generate_report --month 12 --year 2024
"""

from django.core.management.base import BaseCommand
from django.db.models import Sum
from billing_app.models import Pago, Cliente, OrdenTecnica
from datetime import datetime, timedelta
import csv

class Command(BaseCommand):
    help = 'Genera reportes de facturación'

    def add_arguments(self, parser):
        parser.add_argument('--month', type=int, default=None)
        parser.add_argument('--year', type=int, default=datetime.now().year)
        parser.add_argument('--output', type=str, default='reporte.csv')

    def handle(self, *args, **options):
        month = options['month'] or datetime.now().month
        year = options['year']
        output = options['output']

        # Calcular período
        fecha_inicio = datetime(year, month, 1)
        if month == 12:
            fecha_fin = datetime(year + 1, 1, 1)
        else:
            fecha_fin = datetime(year, month + 1, 1)
        fecha_fin = fecha_fin - timedelta(seconds=1)

        # Datos
        total_clientes = Cliente.objects.count()
        pagos = Pago.objects.filter(fecha__range=[fecha_inicio, fecha_fin])
        total_pagos = pagos.aggregate(Sum('monto'))['monto__sum'] or 0
        total_transacciones = pagos.count()
        ots = OrdenTecnica.objects.filter(pagada=True, fecha_creacion__range=[fecha_inicio, fecha_fin])

        # Escribir CSV
        with open(output, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Reporte de Facturación', f'{month}/{year}'])
            writer.writerow([])
            writer.writerow(['Métrica', 'Valor'])
            writer.writerow(['Total Clientes', total_clientes])
            writer.writerow(['Total Pagos', total_transacciones])
            writer.writerow(['Monto Total', f'S/. {total_pagos:.2f}'])
            writer.writerow(['OTs Pagadas', ots.count()])
            writer.writerow(['Ingresos OTs', f'S/. {ots.aggregate(Sum("monto"))["monto__sum"] or 0:.2f}'])

        self.stdout.write(self.style.SUCCESS(f'✓ Reporte guardado en {output}'))


# ========================
# Archivos de Instalación
# ========================

"""
Crear directorios de management commands:

mkdir -p billing_app/management
mkdir -p billing_app/management/commands
touch billing_app/management/__init__.py
touch billing_app/management/commands/__init__.py

Luego mover los scripts anteriores a:
billing_app/management/commands/encrypt_passwords.py
billing_app/management/commands/create_indexes.py
billing_app/management/commands/generate_report.py
"""
