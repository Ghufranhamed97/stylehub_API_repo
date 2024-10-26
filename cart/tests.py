
class CartTests(TestCase):
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
        
        # Create cart first
        response = self.client.post('/api/cart/')
        self.cart_item = None

    def test_update_quantity(self):
        # First add item to cart
        add_response = self.client.post('/api/cart/add_item/', {
            'product_id': self.product.id,
            'quantity': 1
        })
        self.cart_item = add_response.json()
        
        # Then update quantity
        response = self.client.post('/api/cart/update_quantity/', {
            'item_id': self.cart_item['id'],
            'quantity': 3
        })
        self.assertEqual(response.status_code, 200)