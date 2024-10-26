from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Shop, ShopProduct
from .serializers import ShopSerializer, ShopProductSerializer
from products.models import Product

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    # ... (rest of the code remains the same)
    @action(detail=True, methods=['post'])
    def add_product(self, request, pk=None):
        shop = self.get_object()
        product_id = request.data.get('product_id')
        stock = request.data.get('stock', 0)
        price = request.data.get('price')

        if not all([product_id, price]):
            return Response({"error": "Product ID and price are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        shop_product, created = ShopProduct.objects.get_or_create(
            shop=shop,
            product=product,
            defaults={'stock': stock, 'price': price}
        )

        if not created:
            shop_product.stock = stock
            shop_product.price = price
            shop_product.save()

        serializer = ShopProductSerializer(shop_product)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        shop = self.get_object()
        shop_products = ShopProduct.objects.filter(shop=shop)
        serializer = ShopProductSerializer(shop_products, many=True)
        return Response(serializer.data)
    
    
    
    
    