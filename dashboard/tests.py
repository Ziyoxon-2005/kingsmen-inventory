from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
import os
from .models import Product, Order

@override_settings(
    STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage',
    TESTING=True
)
class DashboardTests(TestCase):
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
        self.order = Order.objects.create(
            name=self.product,
            customer=self.user,
            order_quantity=2
        )

    def test_login_required(self):
        response = self.client.get(reverse('dashboard-index'))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_access(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard-index'))
        self.assertEqual(response.status_code, 200)

    def test_context_data(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard-index'))
        self.assertTrue('workers_count' in response.context)
        self.assertTrue('orders_count' in response.context)
        self.assertTrue('products_count' in response.context)

    def test_index_view_with_authentication(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard-index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/index.html')

    def test_index_view_without_authentication(self):
        response = self.client.get(reverse('dashboard-index'))
        self.assertEqual(response.status_code, 302)

    def test_staff_detail_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard-staff-detail', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/staff_detail.html')

    def test_product_detail_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard-product-detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/product_detail.html')

    def test_order_detail_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard-order-detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/order_detail.html')

    def test_dashboard_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard-index'))
        self.assertEqual(response.status_code, 200)

    def test_product_creation(self):
        product = Product.objects.get(name='Test Product')
        self.assertEqual(product.quantity, 10)
