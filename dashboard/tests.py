from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Order

class DashboardTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.product = Product.objects.create(
            name='Test Product',
            quantity=10
        )
        
    def test_login_required(self):
        response = self.client.get(reverse('dashboard-index'))
        self.assertEqual(response.status_code, 302)
        
    def test_authenticated_access(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard-index'))
        self.assertEqual(response.status_code, 200)
        
    def test_product_creation(self):
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.first().name, 'Test Product')
