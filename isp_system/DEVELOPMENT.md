# Instrucciones de Desarrollo - ISP Management System 2026

## 🔧 Configuración del Entorno

### Activar Entorno Virtual

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

## ▶️ Ejecutar el Servidor

```bash
python manage.py runserver
```

El servidor estará disponible en: `http://localhost:8000`

## 🗄️ Comandos de Base de Datos

### Crear nuevas migraciones
```bash
python manage.py makemigrations
```

### Aplicar migraciones
```bash
python manage.py migrate
```

### Ver estado de migraciones
```bash
python manage.py showmigrations
```

### Revertir una migración
```bash
python manage.py migrate isp_app 0001  # Revertir a específica
```

## 🧪 Testing

### Ejecutar todas las pruebas
```bash
python manage.py test
```

### Ejecutar pruebas de una app específica
```bash
python manage.py test isp_app
```

### Ejecutar una clase de test específica
```bash
python manage.py test isp_app.tests.DistritoModelTest
```

## 🐚 Django Shell

Acceder a la consola interactiva de Django:

```bash
python manage.py shell
```

Ejemplos de uso:

```python
from isp_app.models import Cliente, Distrito, Pago

# Crear un distrito
distrito = Distrito.objects.create(nombre="San Isidro")

# Consultar clientes
clientes = Cliente.objects.filter(estado_cliente="Activo")

# Contar registros
total_pagos = Pago.objects.count()

# Agregar registros
cliente = Cliente.objects.create(
    dni_ruc="12345678901",
    nombres_completos="Juan Pérez García",
    numero_casa="123",
    telf="987654321"
)
```

## 📊 Admin Panel

Acceder al panel de administración:
```
http://localhost:8000/admin/
```

**Credenciales:**
- Usuario: `admin`
- Contraseña: `admin123`

## 🆕 Crear Superuser

```bash
python manage.py createsuperuser
```

## 📦 Gestionar Dependencias

### Listar paquetes instalados
```bash
pip list
```

### Exportar dependencias
```bash
pip freeze > requirements.txt
```

### Instalar nuevos paquetes
```bash
pip install nombre_paquete==version
```

## 🔍 Linting y Formateo

### Verificar sintaxis
```bash
python -m py_compile isp_app/models.py
```

## 📝 Crear Nuevas Vistas

1. Agregar vista en `isp_app/views.py`
2. Registrar URL en `isp_app/urls.py`
3. Crear template HTML en `templates/isp_app/`

Ejemplo:

```python
# views.py
from django.views.generic import ListView
from .models import Cliente

class ClienteListView(ListView):
    model = Cliente
    template_name = 'isp_app/cliente_list.html'
    context_object_name = 'clientes'
    paginate_by = 20
```

```python
# urls.py
path('clientes/', views.ClienteListView.as_view(), name='cliente-list'),
```

## 📄 Crear Nuevos Formularios

```python
# forms.py
from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombres_completos', 'dni_ruc', 'telf']
```

## 🎨 Personalizar Estilos

Editar: `static/css/style.css`

Los colores principales están definidos en variables CSS:
```css
:root {
    --primary-color: #2c3e50;
    --secondary-color: #3498db;
    --success-color: #27ae60;
    --danger-color: #e74c3c;
    --warning-color: #f39c12;
}
```

## 🔧 JavaScript Personalizado

Editar: `static/js/main.js`

Funciones disponibles:
- `confirmDelete()` - Confirmación de eliminación
- `formatCurrency()` - Formato de moneda
- `formatDate()` - Formato de fecha
- `filterTable()` - Búsqueda en tablas
- `exportTableToCSV()` - Exportar a CSV
- `printPage()` - Imprimir página

## 🌐 Variables de Entorno (Futuro)

Crear archivo `.env`:
```
DEBUG=True
SECRET_KEY=tu-clave-secreta
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 🚀 Despliegue en Producción

### Usando Gunicorn

```bash
pip install gunicorn
gunicorn isp_project.wsgi:application --bind 0.0.0.0:8000
```

### Usando Nginx como proxy inverso

Configurar `nginx.conf` para redirigir a Gunicorn.

## 📚 Recursos Útiles

- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap 5](https://getbootstrap.com/)
- [Font Awesome](https://fontawesome.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)

## ⚠️ Troubleshooting

### "No module named 'django'"
```bash
pip install Django==4.2.8
```

### Base de datos bloqueada
```bash
rm db.sqlite3
python manage.py migrate
```

### Puerto 8000 en uso
```bash
python manage.py runserver 8001
```

### Plantillas no se actualizan
- Reiniciar servidor Django
- Limpiar caché del navegador (Ctrl+Shift+Delete)

---

**Última actualización**: 24 de Enero, 2026
