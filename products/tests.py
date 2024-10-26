# products/tests.py

from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import Product, Category

class ProductTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        # Create test category first
        self.category = Category.objects.create(name='Test Category')
        
        # Update product data to use category instance
        self.product_data = {
            'name': 'Test Product',
            'description': 'Test Description',
            'price': '99.99',
            'category': self.category,  # Use category instance, not ID
            'gender': 'U',
            'is_accessory': False,
            'is_shoe': False,
            'stock': 10
        }

    def test_create_product(self):
        data = self.product_data.copy()
        data['category'] = self.category.id  # Use category ID for API request
        response = self.client.post('/api/products/', data)
        self.assertEqual(response.status_code, 201)

    def test_product_filters(self):
        product = Product.objects.create(**self.product_data)
        response = self.client.get(f'/api/products/?category={self.category.id}')
        self.assertEqual(response.status_code, 200)