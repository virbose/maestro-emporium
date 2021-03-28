from _decimal import ROUND_HALF_UP
from decimal import Decimal
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Product(models.Model):
    name = models.CharField(max_length=250)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f'{self.name} - £{self.item_price}'


class Cart(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    items = models.ManyToManyField(Product, through='CartItem')

    def __str__(self) -> str:
        return f'Cart Created on {self.created.isoformat()}'

    
    @property
    def cart_total(self) -> Decimal:
        cart_items = self.cartitem_set.all().values('product__item_price', 'item_qty')
        cart_sum = sum([i.get('product__item_price') * i.get('item_qty') for i in cart_items]) or Decimal(0)
        return cart_sum.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    @property
    def items_in_cart(self) -> int:
        return  sum(self.cartitem_set.all().values_list('item_qty', flat=True)) or 0
            

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now=True)
    item_qty = models.IntegerField(default=1)

    def __str__(self) -> str:
        return f'{self.product.name} - {self.item_qty}'

    class Meta:
        unique_together = ('cart', 'product',)
