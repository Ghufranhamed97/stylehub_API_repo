# shops/management/commands/create_test_shops.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from shops.models import Shop, ShopProduct
from products.models import Product
import random
from decimal import Decimal

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates test shops with products'

    def handle(self, *args, **kwargs):
        # Create test user if not exists
        username = 'shopowner'
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': f'{username}@example.com',
                'is_staff': True
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            self.stdout.write(f'Created user: {username}')

        # Create test shop
        shop, created = Shop.objects.get_or_create(
            name="Fashion Hub",
            defaults={
                'owner': user,
                'description': "Your one-stop fashion destination",
                'address': "123 Fashion Street",
                'phone': "1234567890",
                'email': "fashion@hub.com"
            }
        )
        if created:
            self.stdout.write(f'Created shop: {shop.name}')

        # Add products to shop
        products = Product.objects.all()
        for product in products[:20]:  # Add first 20 products
            shop_product, created = ShopProduct.objects.get_or_create(
                shop=shop,
                product=product,
                defaults={
                    'stock': random.randint(10, 100),
                    'price': Decimal(str(round(float(product.price) * random.uniform(0.9, 1.2), 2)))
                }
            )
            if created:
                self.stdout.write(f'Added product to shop: {product.name}')

        self.stdout.write(self.style.SUCCESS('Successfully created test shop data'))