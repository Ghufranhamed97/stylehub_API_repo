# shops/urls.py

from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ShopViewSet

router = DefaultRouter()
router.register('', ShopViewSet, basename='shop')

urlpatterns = router.urls