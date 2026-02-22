"""
Script para cargar datos de prueba en el sistema ISP
Ejecutar: python manage.py shell < seed_data.py
"""

from isp_app.models import (
    Distrito, Sector, Via, Sede, Cliente, PlanInternet,
    ServicioActivo, Personal, Pago, ItemSeriado, MaterialCatalogo,
    CajaNap, Mufa, FibraTramo
)
from datetime import datetime, timedelta
import random

print("Iniciando carga de datos de prueba...")

# ==================== MODULO 01: GEOGRÁFICO ====================

print("\n[1/7] Creando Distritos...")
distritos = [
    Distrito.objects.create(nombre="San Isidro"),
    Distrito.objects.create(nombre="Miraflores"),
    Distrito.objects.create(nombre="La Molina"),
    Distrito.objects.create(nombre="Surco"),
]

print("\n[2/7] Creando Sectores...")
sector_data = {
    distritos[0]: ["Centro", "Norte", "Sur"],
    distritos[1]: ["Costanera", "Mercantil", "Residencial"],
    distritos[2]: ["Casco Urbano", "Periférico"],
    distritos[3]: ["Comercial", "Residencial"],
}

sectores = []
for distrito, nombres in sector_data.items():
    for nombre in nombres:
        sectores.append(Sector.objects.create(distrito=distrito, nombre=nombre))

print("\n[3/7] Creando Vías...")
vias = []
tipos_via = ["Avenida", "Jiron", "Calle", "Pasaje"]
nombres_comunes = ["Principal", "Central", "Libertad", "Indep", "Comercio", "Paz", "Progreso", "Reforma"]

for sector in sectores[:10]:
    for i in range(2):
        tipo = random.choice(tipos_via)
        nombre = f"{random.choice(nombres_comunes)} {i+1}"
        vias.append(Via.objects.create(sector=sector, tipo_via=tipo, nombre=nombre))

# ==================== MODULO 04: COMERCIAL ====================

print("\n[4/7] Creando Planes de Internet...")
planes = [
    PlanInternet.objects.create(nombre_plan="Básico", mbps=10, precio=49.90),
    PlanInternet.objects.create(nombre_plan="Estándar", mbps=30, precio=79.90),
    PlanInternet.objects.create(nombre_plan="Premium", mbps=50, precio=99.90),
    PlanInternet.objects.create(nombre_plan="Ultra", mbps=100, precio=149.90),
]

print("\n[5/7] Creando Clientes...")
nombres_clientes = [
    "Juan Pérez", "María García", "Carlos López", "Ana Martínez",
    "Roberto Sánchez", "Laura González", "Miguel Rodríguez", "Teresa Fernández",
    "Diego Jiménez", "Sofía Ramírez"
]

clientes = []
for i, nombre in enumerate(nombres_clientes):
    cliente = Cliente.objects.create(
        dni_ruc=f"1234567890{i:02d}",
        nombres_completos=nombre,
        via=random.choice(vias),
        numero_casa=f"{random.randint(100, 9999)}",
        telf=f"9{random.randint(10000000, 99999999)}",
        estado_cliente=random.choice(["Activo", "Suspendido", "Activo"])
    )
    clientes.append(cliente)

# ==================== MODULO 06: RRHH ====================

print("\n[6/7] Creando Personal...")
personal = [
    Personal.objects.create(
        nombres_apellidos="Carlos Técnico",
        dni="20345678901",
        rol="Tecnico"
    ),
    Personal.objects.create(
        nombres_apellidos="Admin Sistema",
        dni="20345678902",
        rol="Admin"
    ),
    Personal.objects.create(
        nombres_apellidos="Soporte Usuario",
        dni="20345678903",
        rol="Soporte"
    ),
]

# ==================== MODULO 05: SERVICIO TÉCNICO ====================

print("\n[7/7] Creando Servicios y Pagos...")

# Crear materiales
material_onu = MaterialCatalogo.objects.create(
    nombre="ONU",
    marca="GPON",
    es_seriado=True
)

# Crear items seriados
for i in range(5):
    ItemSeriado.objects.create(
        material=material_onu,
        nro_serie=f"ONU-2024-{i+1:04d}",
        estado="Almacen"
    )

# Crear servicios
for cliente in clientes[:5]:
    plan = random.choice(planes)
    servicio = ServicioActivo.objects.create(
        cliente=cliente,
        plan=plan,
        tecnico=personal[0],
        via_real_instalacion=random.choice(vias),
        puerto_nap_nro=random.randint(1, 32),
        potencia_dbm=random.uniform(-28, -18),
        lat_instalacion=random.uniform(-12.1, -12.0),
        lon_instalacion=random.uniform(-77.0, -76.9)
    )

# Crear pagos
for cliente in clientes:
    for _ in range(random.randint(1, 3)):
        Pago.objects.create(
            cliente=cliente,
            monto=random.choice([49.90, 79.90, 99.90, 149.90]),
            metodo=random.choice(["Efectivo", "Transferencia", "Tarjeta"]),
            referencia=f"REF-{random.randint(100000, 999999)}"
        )

print("\n✅ ¡Carga de datos completada exitosamente!")
print(f"   - Distritos: {Distrito.objects.count()}")
print(f"   - Sectores: {Sector.objects.count()}")
print(f"   - Vías: {Via.objects.count()}")
print(f"   - Planes: {PlanInternet.objects.count()}")
print(f"   - Clientes: {Cliente.objects.count()}")
print(f"   - Personal: {Personal.objects.count()}")
print(f"   - Servicios: {ServicioActivo.objects.count()}")
print(f"   - Pagos: {Pago.objects.count()}")
print(f"   - Items Seriados: {ItemSeriado.objects.count()}")
print("\n🌐 Accede a: http://localhost:8000/")
print("📊 Admin: http://localhost:8000/admin/")
