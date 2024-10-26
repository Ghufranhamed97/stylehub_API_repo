# orders/management/commands/create_test_orders.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from orders.models import Order, OrderItem
from products.models import Product
import random
from decimal import Decimal

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates test orders'

    def handle(self, *args, **kwargs):
        # Get or create test user
        username = 'customer'
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': f'{username}@example.com'
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            self.stdout.write(f'Created user: {username}')

        # Create test orders
        products = list(Product.objects.all())
        
        for i in range(5):  # Create 5 orders
            order = Order.objects.create(
                user=user,
                status=random.choice(['pending', 'processing', 'shipped', 'delivered']),
                total_price=Decimal('0.00')
            )
            
            # Add 2-5 random products to each order
            num_products = random.randint(2, 5)
            total_price = Decimal('0.00')
            
            for _ in range(num_products):
                product = random.choice(products)
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
            self.stdout.write(f'Created order {i+1} with {num_products} items')

        self.stdout.write(self.style.SUCCESS('Successfully created test orders'))