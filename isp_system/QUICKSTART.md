#!/usr/bin/env python
"""
GUÍA RÁPIDA DE INICIO - ISP Management System 2026
====================================================

Este archivo contiene las instrucciones esenciales para comenzar a usar el sistema.
"""

# ============================================================================
# 1. INSTALACIÓN INICIAL
# ============================================================================

print("""
┌─────────────────────────────────────────────────────────────────┐
│                 INSTALACIÓN INICIAL                             │
└─────────────────────────────────────────────────────────────────┘

Paso 1: Navega al directorio del proyecto
    cd c:\\Users\\X10\\Pictures\\new\\ap\\isp_system

Paso 2: Activa el entorno virtual
    Windows:
        .venv\\Scripts\\activate
    
    Linux/Mac:
        source .venv/bin/activate

Paso 3: Verifica que Django esté instalado
    pip list | grep Django

Paso 4: Inicia el servidor
    python manage.py runserver

Resultado esperado:
    Listening on http://127.0.0.1:8000/
""")

# ============================================================================
# 2. ACCESO A LA APLICACIÓN
# ============================================================================

print("""
┌─────────────────────────────────────────────────────────────────┐
│                 ACCESO A LA APLICACIÓN                          │
└─────────────────────────────────────────────────────────────────┘

Dashboard Principal:
    URL: http://localhost:8000/
    Vista: Dashboard con estadísticas

Admin Panel:
    URL: http://localhost:8000/admin/
    Usuario: admin
    Contraseña: admin123

Módulos disponibles en el menú:
    ✓ Geográfico (Distritos, Sectores, Vías)
    ✓ Infraestructura (Sedes)
    ✓ Red Externa (Mufas, Cajas NAP, Fibra)
    ✓ Comercial (Clientes, Planes)
    ✓ Técnico (Servicios, Materiales, Items)
    ✓ RRHH (Personal)
    ✓ Finanzas (Pagos)
    ✓ Reportes (Estadísticas generales)
""")

# ============================================================================
# 3. CARGAR DATOS DE PRUEBA
# ============================================================================

print("""
┌─────────────────────────────────────────────────────────────────┐
│            CARGAR DATOS DE PRUEBA (RECOMENDADO)                 │
└─────────────────────────────────────────────────────────────────┘

El script seed_data.py carga automáticamente:
    - 4 Distritos
    - 10 Sectores
    - 20 Vías
    - 4 Planes de Internet
    - 10 Clientes
    - 3 Personal
    - Servicios y Pagos relacionados

Opción 1: Ejecutar desde Django Shell
    python manage.py shell
    >>> exec(open('seed_data.py').read())

Opción 2: Ejecutar script directamente
    python -c "import django; django.setup(); exec(open('seed_data.py').read())"

Opción 3: A través de SQL
    - Ver db.sqlite3 en tu IDE favorito
""")

# ============================================================================
# 4. NAVEGACIÓN POR LA APLICACIÓN
# ============================================================================

print("""
┌─────────────────────────────────────────────────────────────────┐
│          FLUJO DE NAVEGACIÓN RECOMENDADO                        │
└─────────────────────────────────────────────────────────────────┘

PRIMERA VEZ - Conocer el sistema:
    1. Ir a Dashboard ( / )
    2. Revisar estadísticas
    3. Hacer clic en "Ver Todos" de cada módulo
    4. Explorar formularios de creación

CREAR DATOS:
    1. Geográfico: Crear Distrito → Sector → Vía
    2. Comercial: Crear Planes → Clientes
    3. Técnico: Crear Servicios
    4. Finanzas: Registrar Pagos

CONSULTAR INFORMACIÓN:
    1. Hacer clic en tarjetas o filas para ver detalles
    2. Usar filtros en listas
    3. Navegar entre relacionamientos
    4. Ver historial de transacciones

REPORTES:
    - Acceder a Reportes en el menú
    - Ver gráficos de clientes, servicios, pagos
    - Imprimir reportes
""")

# ============================================================================
# 5. FUNCIONALIDADES CLAVE
# ============================================================================

print("""
┌─────────────────────────────────────────────────────────────────┐
│               FUNCIONALIDADES CLAVE                             │
└─────────────────────────────────────────────────────────────────┘

MÓDULO GEOGRÁFICO:
    ✓ Crear jerarquía: Distrito > Sector > Vía
    ✓ Visualizar cantidad de sub-niveles
    ✓ Modificar información
    ✓ Eliminar registros con confirmación

MÓDULO COMERCIAL:
    ✓ Registrar clientes con dirección completa
    ✓ Crear planes con velocidad y precio
    ✓ Filtrar clientes por estado (Activo/Suspendido/Retirado)
    ✓ Ver historial de servicios y pagos por cliente

MÓDULO TÉCNICO:
    ✓ Instalar servicios con GPS real
    ✓ Registrar potencia en dBm
    ✓ Asignar ONU con número de serie
    ✓ Vincular con Caja NAP específica

MÓDULO FINANZAS:
    ✓ Registrar pagos (Efectivo/Transferencia/Tarjeta/Cheque)
    ✓ Incluir referencia de pago
    ✓ Ver historial por cliente
    ✓ Imprimir recibos

PANEL ADMIN:
    ✓ Acceso completo a todos los modelos
    ✓ Búsqueda avanzada
    ✓ Filtros personalizados
    ✓ Edición masiva
""")

# ============================================================================
# 6. COMANDOS ÚTILES
# ============================================================================

print("""
┌─────────────────────────────────────────────────────────────────┐
│               COMANDOS ÚTILES                                   │
└─────────────────────────────────────────────────────────────────┘

Servidor:
    python manage.py runserver
    python manage.py runserver 8080  # Puerto personalizado
    python manage.py runserver 0.0.0.0:8000  # Acceso remoto

Base de datos:
    python manage.py migrate  # Aplicar migraciones
    python manage.py makemigrations  # Crear migraciones
    python manage.py sqlmigrate isp_app 0001  # Ver SQL
    
Admin:
    python manage.py createsuperuser  # Crear nuevo admin
    
Shell:
    python manage.py shell  # Consola interactiva
    python manage.py dbshell  # Shell de BD

Testing:
    python manage.py test  # Ejecutar tests
    python manage.py test isp_app  # Tests de app
    
Limpieza:
    python manage.py flush  # Limpiar BD
    python manage.py collectstatic  # Recolectar estáticos
""")

# ============================================================================
# 7. EJEMPLOS DE USO EN DJANGO SHELL
# ============================================================================

print("""
┌─────────────────────────────────────────────────────────────────┐
│          EJEMPLOS EN DJANGO SHELL                               │
└─────────────────────────────────────────────────────────────────┘

CREAR DATOS:
    from isp_app.models import *
    
    # Crear distrito
    d = Distrito.objects.create(nombre="Nuevo Distrito")
    
    # Crear cliente
    c = Cliente.objects.create(
        dni_ruc="20123456789",
        nombres_completos="Juan Pérez",
        numero_casa="123",
        telf="987654321"
    )

CONSULTAR DATOS:
    # Todos los registros
    clientes = Cliente.objects.all()
    
    # Filtrar por estado
    activos = Cliente.objects.filter(estado_cliente="Activo")
    
    # Contar
    total = Cliente.objects.count()
    
    # Buscar específico
    cliente = Cliente.objects.get(dni_ruc="20123456789")

RELACIONES:
    # Servicios de un cliente
    cliente = Cliente.objects.first()
    servicios = cliente.servicios_activos.all()
    
    # Pagos de cliente
    pagos = cliente.pagos.all()
    total_pagos = pagos.aggregate(Sum('monto'))

ACTUALIZAR:
    cliente.estado_cliente = "Suspendido"
    cliente.save()

ELIMINAR:
    cliente.delete()
""")

# ============================================================================
# 8. TROUBLESHOOTING
# ============================================================================

print("""
┌─────────────────────────────────────────────────────────────────┐
│               SOLUCIÓN DE PROBLEMAS                             │
└─────────────────────────────────────────────────────────────────┘

Problema: "Puerto 8000 en uso"
    Solución: python manage.py runserver 8001

Problema: "No hay datos en el sitio"
    Solución: Ejecutar seed_data.py para cargar datos de prueba

Problema: "Plantillas no se actualizan"
    Solución: Reiniciar servidor y limpiar caché del navegador

Problema: "Error de base de datos"
    Solución: 
        python manage.py migrate
        python manage.py migrate isp_app

Problema: "Error 404 en URLs"
    Solución: Verificar que las URLs estén bien registradas en urls.py

Problema: "Olvidé contraseña admin"
    Solución: 
        python manage.py changepassword admin
""")

# ============================================================================
# 9. INFORMACIÓN IMPORTANTE
# ============================================================================

print("""
┌─────────────────────────────────────────────────────────────────┐
│            INFORMACIÓN IMPORTANTE                               │
└─────────────────────────────────────────────────────────────────┘

ARCHIVOS CONFIGURACIÓN:
    • isp_project/settings.py - Configuración general
    • isp_project/urls.py - URLs principales
    • isp_app/urls.py - URLs de la app
    • requirements.txt - Dependencias

ESTRUCTURA BASE DE DATOS:
    • db.sqlite3 - Base de datos
    • isp_app/migrations/ - Historial de cambios

ARCHIVOS ESTÁTICOS:
    • static/css/style.css - Estilos personalizados
    • static/js/main.js - JavaScript funcional
    • templates/ - Plantillas HTML

DOCUMENTACIÓN:
    • README.md - Guía general
    • DEVELOPMENT.md - Guía de desarrollo
    • ENTREGA.md - Resumen de entrega
    • Este archivo - Quick start
""")

# ============================================================================
# 10. PRÓXIMOS PASOS
# ============================================================================

print("""
┌─────────────────────────────────────────────────────────────────┐
│            PRÓXIMOS PASOS RECOMENDADOS                          │
└─────────────────────────────────────────────────────────────────┘

CORTO PLAZO:
    ✓ Ejecutar seed_data.py para cargar datos
    ✓ Explorar Dashboard y todos los módulos
    ✓ Probar crear/editar/eliminar registros
    ✓ Revisar panel Admin en http://localhost:8000/admin/

MEDIANO PLAZO:
    ✓ Personalizar estilos en static/css/style.css
    ✓ Agregar más campos según necesidades
    ✓ Crear reportes personalizados
    ✓ Integrar con sistemas externos

LARGO PLAZO:
    ✓ Pasar a base de datos PostgreSQL
    ✓ Implementar autenticación avanzada
    ✓ Crear API REST
    ✓ Agregar geolocalización
    ✓ Implementar notificaciones por email/WhatsApp

¡CUALQUIER CONSULTA, REVISAR LA DOCUMENTACIÓN EN README.md!
""")

print("\n" + "="*65)
print("ISP Management System 2026 - Ready to use!")
print("="*65 + "\n")
