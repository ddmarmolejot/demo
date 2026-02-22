"""
Tests for ISP App
"""
from django.test import TestCase
from django.urls import reverse
from .models import Distrito, Sector, Via, Cliente, PlanInternet


class DistritoModelTest(TestCase):
    """Test for Distrito model"""
    
    def setUp(self):
        self.distrito = Distrito.objects.create(nombre="San Isidro")
    
    def test_distrito_creation(self):
        self.assertTrue(isinstance(self.distrito, Distrito))
        self.assertEqual(str(self.distrito), "San Isidro")


class ClienteModelTest(TestCase):
    """Test for Cliente model"""
    
    def setUp(self):
        self.distrito = Distrito.objects.create(nombre="Lima")
        self.sector = Sector.objects.create(distrito=self.distrito, nombre="Centro")
        self.via = Via.objects.create(sector=self.sector, tipo_via="Calle", nombre="Principal")
        self.cliente = Cliente.objects.create(
            dni_ruc="12345678901",
            nombres_completos="Juan Pérez",
            via=self.via,
            numero_casa="123",
            telf="987654321"
        )
    
    def test_cliente_creation(self):
        self.assertTrue(isinstance(self.cliente, Cliente))
        self.assertEqual(self.cliente.estado_cliente, "Activo")


class DistritoListViewTest(TestCase):
    """Test for Distrito List View"""
    
    def setUp(self):
        Distrito.objects.create(nombre="District 1")
        Distrito.objects.create(nombre="District 2")
    
    def test_view_url_exists(self):
        response = self.client.get(reverse('distrito-list'))
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('distrito-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'isp_app/geografico/distrito_list.html')
