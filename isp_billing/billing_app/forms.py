from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from decimal import Decimal
from .models import (
    Distrito, Sector, Via, Cliente, Plan, ClientePlan, OrdenTecnica,
    Servicio, OrdenTecnicaConcepto, SerieCorrelativo,
    MikrotikConfig, Tecnico, EgresoConcepto, Egreso, AppRole, UserRole,
    CompanySettings
)


class ClienteForm(forms.ModelForm):
    """Formulario de cliente con validaciones de técnica de red"""
    distrito = forms.ModelChoiceField(
        queryset=Distrito.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    sector = forms.ModelChoiceField(
        queryset=Sector.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )

    class Meta:
        model = Cliente
        fields = [
            'apellidos', 'nombres', 'dni', 'celular', 'distrito',
            'sector', 'via', 'referencia', 'estado_activo',
            'tipo_conexion', 'usuario_pppoe', 'password_pppoe',
            'ip_asignada', 'mikrotik_vinculado'
        ]
        widgets = {
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'celular': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '9 dígitos'}
            ),
            'via': forms.Select(attrs={'class': 'form-select'}),
            'referencia': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 2}
            ),
            'tipo_conexion': forms.Select(
                attrs={
                    'class': 'form-select',
                    'onchange': 'toggleTechFields()'
                }
            ),
            'estado_activo': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'usuario_pppoe': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Usuario o ID'
                }
            ),
            'password_pppoe': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Contraseña será encriptada'
                }
            ),
            'ip_asignada': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '192.168.1.1'
                }
            ),
            'mikrotik_vinculado': forms.Select(
                attrs={'class': 'form-select'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'distrito' in self.data:
            try:
                distrito_id = int(self.data.get('distrito'))
                self.fields['sector'].queryset = (
                    Sector.objects.filter(
                        distrito_id=distrito_id
                    ).order_by('nombre')
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.via:
            self.fields['sector'].queryset = (
                self.instance.via.sector.distrito.sectores.all()
            )

        if 'sector' in self.data:
            try:
                sector_id = int(self.data.get('sector'))
                self.fields['via'].queryset = (
                    Via.objects.filter(
                        sector_id=sector_id
                    ).order_by('nombre')
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.via:
            self.fields['via'].queryset = self.instance.via.sector.vias.all()

    def save(self, commit=True):
        """Encripta contraseña antes de guardar"""
        instance = super().save(commit=False)
        if self.cleaned_data.get('password_pppoe'):
            instance.set_pppoe_password(self.cleaned_data['password_pppoe'])
        if commit:
            instance.save()
        return instance


class ClientePlanForm(forms.ModelForm):
    """Formulario para agregar plan a cliente con validaciones"""
    
    class Meta:
        model = ClientePlan
        fields = ['plan', 'fecha_inicio', 'fecha_cobranza']
        widgets = {
            'plan': forms.Select(attrs={'class': 'form-select'}),
            'fecha_inicio': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'fecha_cobranza': forms.NumberInput(
                attrs={'class': 'form-control', 'min': 1, 'max': 31}
            ),
        }

    def clean(self):
        """Validaciones cruzadas"""
        cleaned_data = super().clean()
        fecha_cobranza = cleaned_data.get('fecha_cobranza')
        
        if fecha_cobranza and (fecha_cobranza < 1 or fecha_cobranza > 31):
            raise ValidationError('Fecha de cobranza debe estar entre 1 y 31')
        
        return cleaned_data


class OptionalModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def clean(self, value):
        if not value:
            return self.queryset.none()
        if isinstance(value, (list, tuple)):
            value = [item for item in value if item]
        if not value:
            return self.queryset.none()
        return super().clean(value)


class OrdenTecnicaForm(forms.ModelForm):
    monto = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(
            attrs={'class': 'form-control', 'step': '0.01'}
        )
    )
    tipo_trabajo = forms.ChoiceField(
        choices=OrdenTecnicaConcepto.CAT_CHOICES,
        label='Tipo de trabajo',
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    plan_catalogo = OptionalModelMultipleChoiceField(
        queryset=Plan.objects.none(),
        required=False,
        label='Plan a instalar',
        widget=forms.SelectMultiple(attrs={'class': 'form-select'})
    )
    planes_seleccionados = forms.ModelMultipleChoiceField(
        queryset=ClientePlan.objects.none(),
        required=False,
        label='Planes a cortar',
        widget=forms.CheckboxSelectMultiple()
    )
    servicios_seleccionados = forms.ModelMultipleChoiceField(
        queryset=Servicio.objects.none(),
        required=False,
        label='Servicios afectados',
        widget=forms.CheckboxSelectMultiple()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'plan_catalogo' in self.fields:
            field = self.fields['plan_catalogo']
            field.label_from_instance = (
                lambda p: (
                    f"{p.nombre} ({p.servicio.nombre})"
                    if p.servicio else p.nombre
                )
            )
        if 'planes_seleccionados' in self.fields:
            field = self.fields['planes_seleccionados']
            field.label_from_instance = (
                lambda cp: (
                    f"{cp.plan.nombre} ({cp.plan.servicio.nombre})"
                    if cp.plan and cp.plan.servicio else cp.plan.nombre
                )
            )
        if 'servicios_seleccionados' in self.fields:
            field = self.fields['servicios_seleccionados']
            field.label_from_instance = lambda s: s.nombre

    def clean(self):
        cleaned_data = super().clean()
        tipo_trabajo = cleaned_data.get('tipo_trabajo')
        concepto = cleaned_data.get('concepto')
        plan_catalogo = cleaned_data.get('plan_catalogo')

        if concepto and (not tipo_trabajo or
                         concepto.categoria != tipo_trabajo):
            cleaned_data['tipo_trabajo'] = concepto.categoria
            tipo_trabajo = concepto.categoria

        if tipo_trabajo == 'INSTALACION' and not plan_catalogo:
            raise ValidationError('Seleccione un plan para instalación.')
        # Para cortes/averías se permite registrar OT sin plan asociado.

        if tipo_trabajo in ('INSTALACION', 'CORTES') and concepto:
            cleaned_data['monto'] = concepto.precio_sugerido
        elif tipo_trabajo == 'AVERIAS':
            cleaned_data['monto'] = Decimal('0')

        return cleaned_data

    class Meta:
        model = OrdenTecnica
        fields = [
            'concepto', 'plan_asociado', 'servicio_afectado', 'monto',
            'tecnico_asignado',
            'observaciones', 'completada'
        ]
        widgets = {
            'concepto': forms.Select(attrs={'class': 'form-select'}),
            'plan_asociado': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'servicio_afectado': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'monto': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.01'}
            ),
            'tecnico_asignado': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'observaciones': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
            'completada': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }


class TecnicoForm(forms.ModelForm):
    class Meta:
        model = Tecnico
        fields = ['nombre', 'dni', 'celular', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class DistritoForm(forms.ModelForm):
    class Meta:
        model = Distrito
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej: Los Olivos'
                }
            )
        }


class SectorForm(forms.ModelForm):
    class Meta:
        model = Sector
        fields = ['distrito', 'nombre']
        widgets = {
            'distrito': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej: Sector 1'
                }
            )
        }


class ViaForm(forms.ModelForm):
    class Meta:
        model = Via
        fields = ['sector', 'tipo', 'nombre']
        widgets = {
            'sector': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej: Las Palmeras'
                }
            )
        }


class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej: Internet Fibra'
                }
            )
        }


class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['servicio', 'nombre', 'precio']
        widgets = {
            'servicio': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej: 50 Mbps'
                }
            ),
            'precio': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.01'}
            )
        }


class OTConceptoForm(forms.ModelForm):
    class Meta:
        model = OrdenTecnicaConcepto
        fields = ['categoria', 'nombre', 'precio_sugerido']
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'precio_sugerido': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.01'}
            )
        }


class SerieCorrelativoForm(forms.ModelForm):
    class Meta:
        model = SerieCorrelativo
        fields = ['tipo', 'serie', 'ultimo_numero']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'serie': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej: R001'
                }
            ),
            'ultimo_numero': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),
        }


class MikrotikConfigForm(forms.ModelForm):
    """Formulario para configurar MikroTik con encriptación."""

    class Meta:
        model = MikrotikConfig
        fields = [
            'nombre', 'ip_host', 'usuario', 'password',
            'puerto_api', 'activo'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'ip_host': forms.TextInput(attrs={'class': 'form-control'}),
            'usuario': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Contraseña será encriptada'
                }
            ),
            'puerto_api': forms.NumberInput(
                attrs={'class': 'form-control', 'min': 1, 'max': 65535}
            ),
            'activo': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }

    def save(self, commit=True):
        """Encripta contraseña antes de guardar"""
        instance = super().save(commit=False)
        if self.cleaned_data.get('password'):
            instance.set_password(self.cleaned_data['password'])
        if commit:
            instance.save()
        return instance


class EgresoConceptoForm(forms.ModelForm):
    class Meta:
        model = EgresoConcepto
        fields = ['nombre', 'activo']
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej: Combustible'
                }
            ),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


class EgresoForm(forms.ModelForm):
    class Meta:
        model = Egreso
        fields = [
            'fecha', 'tipo_comprobante', 'numero_comprobante',
            'monto', 'concepto', 'responsable', 'observaciones'
        ]
        widgets = {
            'fecha': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'tipo_comprobante': forms.Select(attrs={'class': 'form-select'}),
            'numero_comprobante': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej: F001-000123'
                }
            ),
            'monto': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.01'}
            ),
            'concepto': forms.Select(attrs={'class': 'form-select'}),
            'responsable': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Responsable'}
            ),
            'observaciones': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 2}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['concepto'].queryset = (
            EgresoConcepto.objects.filter(activo=True).order_by('nombre')
        )


class AppRoleForm(forms.ModelForm):
    class Meta:
        model = AppRole
        fields = [
            'nombre',
            'can_cobrar',
            'can_delete_cliente',
            'can_view_deuda',
            'can_manage_ots',
            'can_manage_ajustes',
            'can_manage_caja'
        ]
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej: Administrador'
                }
            ),
            'can_cobrar': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'can_delete_cliente': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'can_view_deuda': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'can_manage_ots': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'can_manage_ajustes': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'can_manage_caja': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }


class UserRoleForm(forms.ModelForm):
    class Meta:
        model = UserRole
        fields = ['user', 'role']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
        }


class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'is_staff', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_staff': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'is_active': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password1') != cleaned.get('password2'):
            self.add_error('password2', 'Las contraseñas no coinciden.')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserEditForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Nueva contraseña',
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'is_staff', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_staff': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'is_active': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 or p2:
            if p1 != p2:
                self.add_error('password2', 'Las contraseñas no coinciden.')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        p1 = self.cleaned_data.get('password1')
        if p1:
            user.set_password(p1)
        if commit:
            user.save()
        return user


class CompanySettingsForm(forms.ModelForm):
    """Formulario para configuración de empresa"""
    class Meta:
        model = CompanySettings
        fields = [
            'nombre_empresa', 'ruc', 'direccion_fiscal',
            'logo', 'telefono', 'email'
        ]
        widgets = {
            'nombre_empresa': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'ruc': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion_fiscal': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
