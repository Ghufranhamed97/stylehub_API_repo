# shops/serializers.py

from rest_framework import serializers
from .models import Shop, ShopProduct
from products.serializers import ProductSerializer

class ShopProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = ShopProduct
        fields = ['id', 'product', 'stock', 'price']

class ShopSerializer(serializers.ModelSerializer):
    products = ShopProductSerializer(source='shopproduct_set', many=True, read_only=True)

    class Meta:
        model = Shop
        fields = ['id', 'name', 'owner', 'description', 'address', 'phone', 
                 'email', 'created_at', 'updated_at', 'products']