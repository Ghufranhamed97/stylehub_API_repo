# orders/management/commands/create_sample_orders.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from orders.models import Order, OrderItem
from products.models import Product
from django.db import transaction
import random
from datetime import timedelta
from django.utils import timezone

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates sample orders for testing'

    def handle(self, *args, **options):
        users = User.objects.all()
        products = Product.objects.all()

        if not users or not products:
            self.stdout.write(self.style.ERROR('Need users and products to create orders'))
            return

        with transaction.atomic():
            for user in users:
                # Create 1-3 orders for each user
                for _ in range(random.randint(1, 3)):
                    # Select 1-5 products for this order
                    order_products = random.sample(list(products), random.randint(1, 5))
                    
                    # Calculate total price and create order
                    total_price = 0
                    order = Order.objects.create(
                        user=user,
                        status=random.choice(['pending', 'processing', 'shipped', 'delivered']),
                        total_price=0,  # Will update after adding items
                        created_at=timezone.now() - timedelta(days=random.randint(0, 30))
                    )

                    # Add products to order
                    for product in order_products:
                        quantity = random.randint(1, 3)
                        price = float(product.price) * quantity
                        total_price += price
                        
                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            quantity=quantity,
                            price=price
                        )
                    
                    # Update order total
                    order.total_price = total_price
                    order.save()

        self.stdout.write(self.style.SUCCESS('Successfully created sample orders'))