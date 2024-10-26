# products/management/commands/create_test_products.py

from django.core.management.base import BaseCommand
from products.models import Category, Product, ProductImage
from django.core.files.base import ContentFile
import random

class Command(BaseCommand):
    help = 'Creates test products and categories'

    def handle(self, *args, **kwargs):
        # First delete all existing categories to avoid conflicts
        Category.objects.all().delete()
        
        # Create main categories
        categories = {
            'Clothing': None,
            'T-Shirts': 'Clothing',
            'Jeans': 'Clothing',
            'Shoes': None,
            'Sneakers': 'Shoes',
            'Boots': 'Shoes',
            'Accessories': None,
            'Hats': 'Accessories',
            'Bags': 'Accessories',
        }
        
        created_categories = {}
        
        # First create parent categories
        for cat_name, parent_name in categories.items():
            if parent_name is None:
                category = Category.objects.create(name=cat_name)
                created_categories[cat_name] = category
                self.stdout.write(f'Created category: {cat_name}')
        
        # Then create subcategories
        for cat_name, parent_name in categories.items():
            if parent_name is not None:
                parent = created_categories[parent_name]
                category = Category.objects.create(
                    name=cat_name,
                    parent=parent
                )
                created_categories[cat_name] = category
                self.stdout.write(f'Created subcategory: {cat_name} under {parent_name}')

        # Create products for each category
        for category in created_categories.values():
            if category.parent is not None:  # Only create products for subcategories
                for i in range(1, 11):
                    product = Product.objects.create(
                        name=f"{category.name} {i}",
                        description=f"Description for {category.name} {i}",
                        price=round(random.uniform(10, 100), 2),
                        category=category,
                        gender=random.choice(['M', 'W', 'K', 'U']),
                        is_accessory=category.parent.name == 'Accessories',
                        is_shoe=category.parent.name == 'Shoes',
                        stock=random.randint(1, 100)
                    )
                    self.stdout.write(f'Created product: {product.name}')

        self.stdout.write(self.style.SUCCESS('Successfully created test data'))