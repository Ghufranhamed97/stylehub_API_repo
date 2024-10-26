# Create this in management/commands/create_test_data.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from shops.models import Shop, ShopProduct
from orders.models import Order, OrderItem
from products.models import Product
from django.db import transaction
import random
from decimal import Decimal

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates test shop products and orders'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating test data...')
        
        with transaction.atomic():
            # Ensure we have a test user
            user, created = User.objects.get_or_create(
                username='testuser1',
                defaults={
                    'email': 'testuser1@example.com',
                    'is_staff': True
                }
            )
            if created:
                user.set_password('TestPass123!')
                user.save()
                self.stdout.write(f'Created test user: {user.username}')

            # Create a shop if none exists
            shop, created = Shop.objects.get_or_create(
                name='Sample Shop',
                defaults={
                    'owner': user,
                    'description': 'A sample shop for testing',
                    'address': '123 Test Street, Test City',
                    'phone': '1234567890',
                    'email': 'shop@example.com'
                }
            )
            if created:
                self.stdout.write(f'Created shop: {shop.name}')

            # Add products to shop
            products = Product.objects.all()[:10]  # Get first 10 products
            for product in products:
                shop_product, created = ShopProduct.objects.get_or_create(
                    shop=shop,
                    product=product,
                    defaults={
                        'stock': random.randint(10, 100),
                        'price': product.price * Decimal(random.uniform(0.9, 1.1))
                    }
                )
                if created:
                    self.stdout.write(f'Added product to shop: {product.name}')

            # Create test order
            order = Order.objects.create(
                user=user,
                status='pending',
                total_price=Decimal('0.00')
            )

            # Add some products to the order
            total_price = Decimal('0.00')
            for product in random.sample(list(products), 3):
                quantity = random.randint(1, 3)
                price = product.price * quantity
                total_price += price
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price
                )

            order.total_price = total_price
            order.save()
            self.stdout.write('Created test order')

        self.stdout.write(self.style.SUCCESS('Successfully created all test data'))