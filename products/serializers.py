# products/serializers.py

from rest_framework import serializers
from .models import Product, Category, ProductImage
from decimal import Decimal

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = ProductImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 
                 'gender', 'is_accessory', 'is_shoe', 'stock', 'images']

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        category, _ = Category.objects.get_or_create(
            name=category_data['name'].lower()
        )
        
        product = Product.objects.create(
            category=category,
            **validated_data
        )
        
        return product

    def update(self, instance, validated_data):
        # Handle category update
        if 'category' in validated_data:
            category_data = validated_data.pop('category')
            category, _ = Category.objects.get_or_create(
                name=category_data['name'].lower()
            )
            instance.category = category
        
        # Update other fields
        for attr, value in validated_data.items():
            if attr == 'price':
                setattr(instance, attr, Decimal(str(value)))
            else:
                setattr(instance, attr, value)
        
        instance.save()
        return instance