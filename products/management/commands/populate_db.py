import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File
from products.models import Product, ProductImage
import random

class Command(BaseCommand):
    help = 'Adds images to existing products'

    def handle(self, *args, **kwargs):
        self.stdout.write('Adding images to products...')

        # Map categories to their image directories
        category_image_dirs = {
            'T-Shirts': 't-shirts',
            'Jeans': 'jeans',
            'Sneakers': 'sneakers',
            'Boots': 'boots',
            'Hats': 'hats',
            'Bags': 'bags',
        }

        sample_image_dir = os.path.join(settings.MEDIA_ROOT, 'sample_images')

        for product in Product.objects.all():
            category_name = product.category.name
            if category_name in category_image_dirs:
                image_subdir = category_image_dirs[category_name]
                category_image_dir = os.path.join(sample_image_dir, image_subdir)
                
                if os.path.exists(category_image_dir):
                    category_images = [f for f in os.listdir(category_image_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
                    
                    if category_images:
                        # Remove existing images
                        product.images.all().delete()
                        
                        # Add 1-3 new images to the product
                        for _ in range(random.randint(1, 3)):
                            image_name = random.choice(category_images)
                            image_path = os.path.join(category_image_dir, image_name)
                            with open(image_path, 'rb') as image_file:
                                product_image = ProductImage(product=product)
                                product_image.image.save(image_name, File(image_file), save=True)
                        
                        self.stdout.write(self.style.SUCCESS(f'Added images to product: {product.name}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'No images found for category: {category_name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Directory not found for category: {category_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'No image directory mapped for category: {category_name}'))

        self.stdout.write(self.style.SUCCESS('Finished adding images to products!'))