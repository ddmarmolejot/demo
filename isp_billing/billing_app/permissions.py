from django.conf import settings
from .models import UserRole

ROLE_DEVELOPER = 'DESARROLLADOR'
ROLE_ADMIN = 'ADMINISTRADOR'
ROLE_USER = 'USUARIO'


def _get_app_role(user):
    if not user or not user.is_authenticated:
        return None
    try:
        return UserRole.objects.select_related('role').get(user=user).role
    except UserRole.DoesNotExist:
        return None


def get_user_role(user):
    if not user or not user.is_authenticated:
        return ROLE_USER
    if user.is_superuser:
        return ROLE_DEVELOPER
    role = _get_app_role(user)
    return role.nombre if role else ROLE_USER


def is_developer(user):
    return get_user_role(user) == ROLE_DEVELOPER


def can_delete_cliente(user):
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return settings.DEBUG
    role = _get_app_role(user)
    return bool(settings.DEBUG and role and role.can_delete_cliente)


def can_cobrar(user):
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    role = _get_app_role(user)
    return bool(role and role.can_cobrar)


def can_manage_ajustes(user):
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    role = _get_app_role(user)
    return bool(role and role.can_manage_ajustes)


def can_manage_caja(user):
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    role = _get_app_role(user)
    return bool(role and role.can_manage_caja)


def can_view_deuda(user):
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    role = _get_app_role(user)
    return bool(role and role.can_view_deuda)
