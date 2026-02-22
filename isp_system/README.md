# ISP Management System 2026 - Sistema de Gestión Integral ISP Total

## 📋 Descripción

Sistema integral de gestión para proveedores de internet (ISP) desarrollado con Django y Bootstrap 5. Implementa todos los módulos solicitados con interfaz web moderna y base de datos relacional completa.

## 🏗️ Estructura de Módulos

### Módulo 01: Núcleo Geográfico (Jerarquía de Ubicación)
- **Distritos**: Nivel jerárquico superior
- **Sectores**: Subdivisión de distritos
- **Vías**: Avenidas, Jirines, Calles, Pasajes y Carreteras

### Módulo 02: Infraestructura Core y Sedes
- **Sedes**: Oficinas administrativas con RUC, número municipal, razón social
- **Servidores Mikrotik**: Gestión de conectividad
- **Equipos OLT/EDFA**: Equipamiento de red

### Módulo 03: Red Externa y GIS (Planta Pasiva)
- **Tramos de Fibra**: Gestión de líneas con múltiples hilos (12, 24, 48, 96, 144)
- **Mufas**: Puntos de distribución (Troncal, Distribución)
- **Cajas NAP**: Network Access Points con geolocalización

### Módulo 04: Comercial y Clientes
- **Planes de Internet**: Velocidades y precios configurables
- **Gestión de Clientes**: Registro completo con direcciones, teléfonos, estado

### Módulo 05: Reporte de Instalación y Servicio Técnico
- **Servicios Activos**: Instalaciones con GPS real, potencia dBm
- **Materiales**: Catálogo con control de ítems seriados
- **Items Seriados**: ONUs, equipos con seguimiento de estado (Almacén, Instalado, Taller)

### Módulo 06: RRHH, Logística y Flota
- **Personal**: Técnicos, Administradores, Soporte
- **Salud y Dotación**: Grupo sanguíneo, SCTR, tallas
- **Vehículos**: Control de flota con SOAT

### Módulo 07: Finanzas y Auditoría
- **Pagos**: Efectivo, Transferencia, Tarjeta, Cheque
- **Logs de Auditoría**: Registro completo de cambios

## 🚀 Instalación Rápida

### Requisitos Previos
- Python 3.10+
- pip o conda

### Pasos de Instalación

1. **Navegar al directorio del proyecto**
```bash
cd c:\Users\X10\Pictures\new\ap\isp_system
```

2. **Activar el entorno virtual**
```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Ejecutar migraciones**
```bash
python manage.py migrate
```

5. **Crear superusuario**
```bash
python manage.py createsuperuser
```

6. **Iniciar servidor**
```bash
python manage.py runserver
```

7. **Acceder a la aplicación**
```
http://localhost:8000/
http://localhost:8000/admin/
```

## 📊 Credenciales Iniciales

- **Usuario**: admin
- **Contraseña**: admin123
- **URL Admin**: http://localhost:8000/admin/

## 🗺️ Mapa de URLs Principales

| Módulo | URL | Descripción |
|--------|-----|-------------|
| Dashboard | `/` | Panel principal |
| Distritos | `/distritos/` | Gestión de distritos |
| Sectores | `/sectores/` | Gestión de sectores |
| Vías | `/vias/` | Gestión de vías |
| Sedes | `/sedes/` | Gestión de sedes |
| Clientes | `/clientes/` | Gestión de clientes |
| Planes | `/planes/` | Gestión de planes |
| Servicios | `/servicios/` | Gestión de servicios |
| Pagos | `/pagos/` | Gestión de pagos |
| Reportes | `/reportes/` | Reportes generales |

## 📁 Estructura del Proyecto

```
isp_system/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── isp_project/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── isp_app/
│   ├── models.py          # 21 modelos de la BD
│   ├── views.py           # Vistas para todos los módulos
│   ├── urls.py            # Rutas de la aplicación
│   ├── forms.py           # Formularios Django
│   ├── admin.py           # Configuración del admin
│   ├── apps.py            # Configuración de la app
│   └── migrations/        # Migraciones de BD
├── static/
│   ├── css/
│   │   └── style.css      # Estilos personalizados
│   └── js/
│       └── main.js        # JavaScript funcional
├── templates/
│   ├── base.html          # Template base
│   └── isp_app/
│       ├── index.html     # Dashboard
│       ├── geografico/    # Templates geográficos
│       ├── infraestructura/
│       ├── red_externa/
│       ├── comercial/
│       ├── tecnico/
│       ├── rrhh/
│       ├── finanzas/
│       └── reportes/
└── .venv/                 # Entorno virtual
```

## 🎨 Características de la Interfaz

- **Diseño Responsivo**: Compatible con desktop, tablet y móvil
- **Navbar de Navegación**: Menú expandible con todos los módulos
- **Dashboard**: Estadísticas principales y acciones rápidas
- **Tablas Interactivas**: Con paginación y filtrado
- **Formularios Validados**: Con manejo de errores
- **Bootstrap 5**: Framework CSS moderno
- **Font Awesome**: 6.4.0 para iconografía

## 🔐 Características de Seguridad

- CSRF Protection
- Validación de formularios servidor-lado
- Autenticación Django
- Permisos basados en roles (en futuras versiones)
- Logs de auditoría

## 📈 Modelos de Datos

Total: **21 Modelos**

1. Distrito
2. Sector
3. Via
4. Sede
5. ServidorMikrotik
6. EquipoOltEdfa
7. FibraTramo
8. Mufa
9. CajaNap
10. PlanInternet
11. Cliente
12. MaterialCatalogo
13. ItemSeriado
14. Personal
15. ServicioActivo
16. PersonalSaludDotacion
17. Vehiculo
18. Pago
19. LogAuditoria

## 🚧 Próximas Mejoras

- [ ] Autenticación de usuarios
- [ ] Sistema de permisos por rol
- [ ] Gráficos en reportes (Chart.js)
- [ ] Geolocalización en tiempo real (Google Maps)
- [ ] Exportación a PDF
- [ ] API REST (Django REST Framework)
- [ ] Soporte multi-idioma
- [ ] Integración con WhatsApp
- [ ] Sistema de notificaciones

## 📝 Notas de Desarrollo

- Base de datos: SQLite (producción usa PostgreSQL)
- Framework: Django 4.2.8
- Frontend: Bootstrap 5 + Vanilla JavaScript
- Servidor: Django Development Server (producción usa Gunicorn/Nginx)

## 👨‍💻 Soporte

Para reportar bugs o sugerencias, contactar al equipo de desarrollo.

## 📄 Licencia

Sistema privado para ISP Total 2026

---

**Última actualización**: 24 de Enero, 2026
