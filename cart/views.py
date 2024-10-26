# cart/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import Product
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Create or get user's cart"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['product_id', 'quantity'],
            properties={
                'product_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, default=1)
            }
        )
    )
    @action(detail=False, methods=['post'])
    def add_item(self, request):
        """Add item to cart"""
        try:
            product_id = request.data.get('product_id')
            quantity = int(request.data.get('quantity', 1))

            if quantity < 1:
                return Response(
                    {'error': 'Quantity must be positive'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            cart, _ = Cart.objects.get_or_create(user=request.user)
            product = get_object_or_404(Product, id=product_id)

            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )

            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            serializer = CartItemSerializer(cart_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Product.DoesNotExist:
            return Response(
                {'error': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError:
            return Response(
                {'error': 'Invalid quantity'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['item_id'],
            properties={
                'item_id': openapi.Schema(type=openapi.TYPE_INTEGER)
            }
        )
    )
    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        """Remove item from cart"""
        try:
            item_id = request.data.get('item_id')
            cart = Cart.objects.get(user=request.user)
            item = get_object_or_404(CartItem, id=item_id, cart=cart)
            item.delete()
            return Response(
                {'message': 'Item removed successfully'},
                status=status.HTTP_200_OK
            )
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Item not found in cart'},
                status=status.HTTP_404_NOT_FOUND
            )

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['item_id', 'quantity'],
            properties={
                'item_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'quantity': openapi.Schema(type=openapi.TYPE_INTEGER)
            }
        )
    )
    @action(detail=False, methods=['post'])
    def update_quantity(self, request):
        """Update item quantity"""
        try:
            item_id = request.data.get('item_id')
            quantity = int(request.data.get('quantity', 0))

            if quantity < 0:
                return Response(
                    {'error': 'Quantity must be non-negative'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            cart = Cart.objects.get(user=request.user)
            item = get_object_or_404(CartItem, id=item_id, cart=cart)

            if quantity == 0:
                item.delete()
                return Response(
                    {'message': 'Item removed from cart'},
                    status=status.HTTP_200_OK
                )

            item.quantity = quantity
            item.save()
            serializer = CartItemSerializer(item)
            return Response(serializer.data)

        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Item not found in cart'},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError:
            return Response(
                {'error': 'Invalid quantity'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'])
    def clear(self, request):
        """Clear all items from cart"""
        cart = Cart.objects.get(user=request.user)
        cart.items.all().delete()
        return Response(
            {'message': 'Cart cleared successfully'},
            status=status.HTTP_200_OK
        )