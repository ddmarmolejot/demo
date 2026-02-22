from django.conf import settings
from django.db.utils import OperationalError, ProgrammingError
from .models import CompanySettings
from .permissions import (
    get_user_role,
    is_developer,
    can_cobrar,
    can_delete_cliente,
    can_manage_ajustes,
    can_manage_caja,
    can_view_deuda,
)


def app_context(request):
    role = get_user_role(getattr(request, 'user', None))
    try:
        company_settings = CompanySettings.get_settings()
    except (OperationalError, ProgrammingError):
        company_settings = None
    return {
        'user_role': role,
        'is_developer': is_developer(getattr(request, 'user', None)),
        'can_cobrar': can_cobrar(getattr(request, 'user', None)),
        'can_delete_cliente': can_delete_cliente(
            getattr(request, 'user', None)
        ),
        'can_manage_ajustes': can_manage_ajustes(
            getattr(request, 'user', None)
        ),
        'can_manage_caja': can_manage_caja(
            getattr(request, 'user', None)
        ),
        'can_view_deuda': can_view_deuda(getattr(request, 'user', None)),
        'is_dev_mode': settings.DEBUG,
        'company_settings': company_settings,
    }
