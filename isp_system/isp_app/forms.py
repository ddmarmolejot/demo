"""
Forms for ISP Management System
"""
from django import forms
from .models import (
    Distrito, Sector, Via, Sede, Cliente, PlanInternet,
    ServicioActivo, Personal, Pago, MaterialCatalogo, ItemSeriado
)


class DistritoForm(forms.ModelForm):
    class Meta:
        model = Distrito
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del distrito'
            })
        }


class SectorForm(forms.ModelForm):
    class Meta:
        model = Sector
        fields = ['distrito', 'nombre']
        widgets = {
            'distrito': forms.Select(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del sector'})
        }


class ViaForm(forms.ModelForm):
    class Meta:
        model = Via
        fields = ['sector', 'tipo_via', 'nombre']
        widgets = {
            'sector': forms.Select(attrs={'class': 'form-control'}),
            'tipo_via': forms.Select(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la vía'})
        }


class SedeForm(forms.ModelForm):
    class Meta:
        model = Sede
        fields = ['via', 'numero_municipal', 'nombre_sede', 'ruc', 'razon_social', 'cert_digital_path']
        widgets = {
            'via': forms.Select(attrs={'class': 'form-control'}),
            'numero_municipal': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_sede': forms.TextInput(attrs={'class': 'form-control'}),
            'ruc': forms.TextInput(attrs={'class': 'form-control'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),
            'cert_digital_path': forms.FileInput(attrs={'class': 'form-control'})
        }


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['dni_ruc', 'nombres_completos', 'via', 'numero_casa', 'mz_lote_int', 'telf', 'estado_cliente']
        widgets = {
            'dni_ruc': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'DNI/RUC', 'min': '0', 'maxlength': '8'}),
            'nombres_completos': forms.TextInput(attrs={'class': 'form-control'}),
            'via': forms.Select(attrs={'class': 'form-control'}),
            'numero_casa': forms.TextInput(attrs={'class': 'form-control'}),
            'mz_lote_int': forms.TextInput(attrs={'class': 'form-control'}),
            'telf': forms.TextInput(attrs={'class': 'form-control'}),
            'estado_cliente': forms.Select(attrs={'class': 'form-control'})
        }


class PlanInternetForm(forms.ModelForm):
    class Meta:
        model = PlanInternet
        fields = ['nombre_plan', 'mbps', 'precio']
        widgets = {
            'nombre_plan': forms.TextInput(attrs={'class': 'form-control'}),
            'mbps': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
        }


class ServicioActivoForm(forms.ModelForm):
    class Meta:
        model = ServicioActivo
        fields = ['cliente', 'plan', 'tecnico', 'via_real_instalacion', 'nap', 'puerto_nap_nro', 'onu_serie', 'potencia_dbm', 'lat_instalacion', 'lon_instalacion']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'plan': forms.Select(attrs={'class': 'form-control'}),
            'tecnico': forms.Select(attrs={'class': 'form-control'}),
            'via_real_instalacion': forms.Select(attrs={'class': 'form-control'}),
            'nap': forms.Select(attrs={'class': 'form-control'}),
            'puerto_nap_nro': forms.NumberInput(attrs={'class': 'form-control'}),
            'onu_serie': forms.Select(attrs={'class': 'form-control'}),
            'potencia_dbm': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'lat_instalacion': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.00000001'}),
            'lon_instalacion': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.00000001'})
        }


class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['cliente', 'monto', 'metodo', 'referencia']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'metodo': forms.Select(attrs={'class': 'form-control'}),
            'referencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Referencia (opcional)'})
        }
