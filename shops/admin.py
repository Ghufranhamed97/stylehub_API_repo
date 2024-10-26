from django.contrib import admin
from .models import Shop

# Register your models here.


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'phone', 'email')
    search_fields = ('name', 'description', 'owner__username')