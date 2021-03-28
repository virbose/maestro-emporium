from django.contrib import admin
from shop.models import Cart, Product, CartItem


class CartAdmin(admin.ModelAdmin):
    readonly_fields = ['created', 'updated']


class ProductAdmin(admin.ModelAdmin):
    pass

class CartItemAdmin(admin.ModelAdmin):
    raw_id_fields = ['cart', 'product']

admin.site.register(Cart, CartAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(CartItem, CartItemAdmin)