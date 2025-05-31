from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile

class UserTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_profile_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('user-profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/profile.html')

    def test_profile_update(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            'username': 'updateduser',
            'phone': '0987654321',
            'address': 'Updated Address'
        }
        response = self.client.post(reverse('user-profile-update'), data)
        self.assertEqual(response.status_code, 302)
        updated_profile = Profile.objects.get(customer=self.user)
        self.assertEqual(updated_profile.phone, '0987654321')
        self.assertEqual(updated_profile.address, 'Updated Address')

    def test_register_view(self):
        response = self.client.get(reverse('user-register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/register.html')

    def test_register_new_user(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password1': 'newpass123',
            'password2': 'newpass123'
        }
        response = self.client.post(reverse('user-register'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())
