"""
Apps configuration for ISP app
"""
from django.apps import AppConfig


class IspAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'isp_app'
    verbose_name = 'Sistema de Gestión ISP'
