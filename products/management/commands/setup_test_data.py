# products/management/commands/setup_test_data.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from products.models import Category, Product, ProductImage
from shops.models import Shop, ShopProduct
from orders.models import Order, OrderItem
from django.db import transaction
from django.core.files.base import ContentFile
import random
from decimal import Decimal
import os
from django.conf import settings
from io import BytesIO
from PIL import Image

User = get_user_model()

class Command(BaseCommand):
    help = 'Sets up complete test data for the e-commerce system'

    def create_media_dirs(self):
        media_root = settings.MEDIA_ROOT
        product_images_dir = os.path.join(media_root, 'product_images')
        os.makedirs(product_images_dir, exist_ok=True)
        return product_images_dir

    def create_sample_image(self, name, color='blue'):
        img = Image.new('RGB', (100, 100), color=color)
        buffer = BytesIO()
        img.save(buffer, format='JPEG')
        img_file = ContentFile(buffer.getvalue(), name=f'{name}.jpg')
        buffer.close()
        return img_file

    def handle(self, *args, **kwargs):
        images_dir = self.create_media_dirs()
        self.stdout.write(f'Using media directory: {images_dir}')

        try:
            with transaction.atomic():
                # Create test users
                self.stdout.write('Creating test users...')
                customer = User.objects.create_user(
                    username='customer',
                    email='customer@example.com',
                    password='customer123',
                    is_staff=True
                )

                # Create categories hierarchy
                categories_data = {
                    'Clothing': {
                        'subcategories': ['T-Shirts', 'Jeans'],
                        'colors': ['red', 'blue', 'green']
                    },
                    'Shoes': {
                        'subcategories': ['Sneakers', 'Boots'],
                        'colors': ['black', 'white', 'brown']
                    },
                    'Accessories': {
                        'subcategories': ['Hats', 'Bags'],
                        'colors': ['yellow', 'purple', 'orange']
                    }
                }

                # Create categories
                self.stdout.write('Creating categories and products...')
                for main_cat, data in categories_data.items():
                    parent_cat = Category.objects.create(name=main_cat)
                    self.stdout.write(f'Created main category: {main_cat}')
                    
                    for sub_cat in data['subcategories']:
                        child_cat = Category.objects.create(
                            name=sub_cat,
                            parent=parent_cat
                        )
                        self.stdout.write(f'Created subcategory: {sub_cat} under {main_cat}')
                        
                        # Create products for each subcategory
                        for i in range(1, 11):
                            product = Product.objects.create(
                                name=f"{sub_cat} {i}",
                                description=f"Description for {sub_cat} {i}",
                                price=Decimal(str(round(random.uniform(10, 100), 2))),
                                category=child_cat,
                                gender=random.choice(['M', 'W', 'K', 'U']),
                                is_accessory='Accessories' in main_cat,
                                is_shoe='Shoes' in main_cat,
                                stock=random.randint(1, 100)
                            )
                            self.stdout.write(f'Created product: {product.name}')
                            
                            # Add images for each product
                            for j in range(random.randint(2, 3)):
                                color = random.choice(data['colors'])
                                image = ProductImage.objects.create(
                                    product=product,
                                    image=self.create_sample_image(
                                        f"{sub_cat.lower()}-{product.id}-{j}",
                                        color
                                    )
                                )
                                self.stdout.write(f'Added image {j+1} to {product.name}')

                # Create shop
                self.stdout.write('Creating shop...')
                shop = Shop.objects.create(
                    name="Fashion Hub",
                    owner=customer,
                    description="Your one-stop fashion destination",
                    address="123 Fashion Street",
                    phone="1234567890",
                    email="fashion@hub.com"
                )

                # Add products to shop
                self.stdout.write('Adding products to shop...')
                for product in Product.objects.all():
                    ShopProduct.objects.create(
                        shop=shop,
                        product=product,
                        stock=random.randint(10, 100),
                        price=Decimal(str(round(float(product.price) * random.uniform(0.9, 1.2), 2)))
                    )

                # Create orders
                self.stdout.write('Creating orders...')
                statuses = ['pending', 'processing', 'shipped', 'delivered']
                products = list(Product.objects.all())
                
                for i in range(5):
                    order = Order.objects.create(
                        user=customer,
                        status=random.choice(statuses),
                        total_price=0
                    )
                    
                    # Add 3-5 random items to order
                    total_price = Decimal('0')
                    for _ in range(random.randint(3, 5)):
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
                    self.stdout.write(f'Created order {i+1}')

                self.stdout.write(self.style.SUCCESS('Successfully created all test data'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
            raise