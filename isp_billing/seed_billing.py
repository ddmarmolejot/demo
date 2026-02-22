import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'isp_billing.settings')
django.setup()

from billing_app.models import Distrito, Sector, Via, Plan, SerieCorrelativo, Servicio

# Servicios
serv_int, _ = Servicio.objects.get_or_create(nombre='Internet')

# Distritos
d1, _ = Distrito.objects.get_or_create(nombre='San Isidro')
d2, _ = Distrito.objects.get_or_create(nombre='Miraflores')

# Sectores
s1, _ = Sector.objects.get_or_create(distrito=d1, nombre='Sector 1')
s2, _ = Sector.objects.get_or_create(distrito=d1, nombre='Sector 2')
s3, _ = Sector.objects.get_or_create(distrito=d2, nombre='Zona A')

# Vías
Via.objects.get_or_create(sector=s1, nombre='Av. Arequipa')
Via.objects.get_or_create(sector=s1, nombre='Calle Las Camelias')
Via.objects.get_or_create(sector=s2, nombre='Jr. Libertad')
Via.objects.get_or_create(sector=s3, nombre='Av. Larco')

# Planes
Plan.objects.get_or_create(servicio=serv_int, nombre='Plan 50 Mbps', precio=50.00)
Plan.objects.get_or_create(servicio=serv_int, nombre='Plan 100 Mbps', precio=80.00)
Plan.objects.get_or_create(servicio=serv_int, nombre='Plan 200 Mbps', precio=120.00)

# Correlativos
SerieCorrelativo.objects.get_or_create(tipo='BOLETA', serie='B001', ultimo_numero=0)
SerieCorrelativo.objects.get_or_create(tipo='FACTURA', serie='F001', ultimo_numero=0)
SerieCorrelativo.objects.get_or_create(tipo='RECIBO', serie='R001', ultimo_numero=0)

# Conceptos OT
from billing_app.models import OrdenTecnicaConcepto
OrdenTecnicaConcepto.objects.get_or_create(nombre='Instalación de Fibra', precio_sugerido=100.00)
OrdenTecnicaConcepto.objects.get_or_create(nombre='Cambio de Router', precio_sugerido=50.00)
OrdenTecnicaConcepto.objects.get_or_create(nombre='Soporte Técnico a Domicilio', precio_sugerido=30.00)

print("Datos iniciales cargados correctamente.")
