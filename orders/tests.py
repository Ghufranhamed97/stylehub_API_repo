# orders/tests.py

class OrderTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        # Create category and product
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            price=99.99,
            category=self.category,
            gender='U',
            stock=10
        )

    def test_create_order(self):
        order_data = {
            'items': [
                {
                    'product': self.product.id,
                    'quantity': 2
                }
            ],
            'total_price': str(self.product.price * 2)
        }
        response = self.client.post('/api/orders/', order_data, format='json')
        self.assertEqual(response.status_code, 201)