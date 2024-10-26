# shops/management/commands/link_products_to_shops.py

from django.core.management.base import BaseCommand
from shops.models import Shop, ShopProduct
from products.models import Product
from django.db import transaction
import random

class Command(BaseCommand):
    help = 'Links products to shops with random stock and prices'

    def handle(self, *args, **options):
        shops = Shop.objects.all()
        products = Product.objects.all()

        if not shops:
            self.stdout.write(self.style.ERROR('No shops found. Please create shops first.'))
            return

        with transaction.atomic():
            for shop in shops:
                # Randomly select 10-20 products for each shop
                selected_products = random.sample(list(products), min(random.randint(10, 20), len(products)))
                
                for product in selected_products:
                    # Create shop product with random stock and slightly modified price
                    price_modifier = random.uniform(0.8, 1.2)  # Price might be 80%-120% of original
                    shop_product = ShopProduct.objects.create(
                        shop=shop,
                        product=product,
                        stock=random.randint(5, 100),
                        price=float(product.price) * price_modifier
                    )

        self.stdout.write(self.style.SUCCESS('Successfully linked products to shops'))