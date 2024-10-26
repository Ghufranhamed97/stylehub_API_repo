# users/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LogoutView, login_view, UserViewSet

router = DefaultRouter()
router.register(r'profile', UserViewSet, basename='user')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', login_view, name='login'),
    path('', include(router.urls)),
]