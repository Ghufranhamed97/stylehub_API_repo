# users/tests.py

class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }

    def test_register(self):
        response = self.client.post('/users/register/', self.user_data)
        self.assertEqual(response.status_code, 201)

    def test_profile(self):
        # Create and login user first
        user = get_user_model().objects.create_user(**self.user_data)
        self.client.force_authenticate(user=user)
        
        # Get profile
        response = self.client.get('/users/profile/')
        self.assertEqual(response.status_code, 200)