from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
import os
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
        
        # Ensure static files directory exists
        os.makedirs(settings.STATIC_ROOT, exist_ok=True)
        
    def test_login_required(self):
        response = self.client.get(reverse('dashboard-index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/user/login/?next=/')
        
    def test_authenticated_access(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard-index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/index.html')
        
    def test_product_creation(self):
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.first().name, 'Test Product')

    def test_context_data(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard-index'))
        self.assertTrue('total_staff' in response.context)
        self.assertTrue('total_product' in response.context)
        self.assertTrue('total_order' in response.context)
        self.assertTrue('orders' in response.context)
        self.assertTrue('products' in response.context)
