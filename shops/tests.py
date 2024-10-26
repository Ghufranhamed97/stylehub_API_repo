# shops/tests.py

from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import Shop

class ShopTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.shop_data = {
            'name': 'Test Shop',
            'description': 'Test Description',
            'address': 'Test Address',
            'phone': '1234567890',
            'email': 'shop@test.com'
        }

    def test_create_shop(self):
        """Test shop creation"""
        response = self.client.post('/api/shops/', self.shop_data)
        self.assertEqual(response.status_code, 201)

    def test_view_shops(self):
        """Test shop listing"""
        response = self.client.get('/api/shops/')
        self.assertEqual(response.status_code, 200)