from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, View

from shop.models import Product, CartItem, Cart


class ShopHomeView(ListView):
    template_name = 'shop/home.html'
    context_object_name = 'products'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart.objects.get(pk=self.request.session.get('cart_id'))

        return context


class AddToCartView(View):
    http_method_names = ['get',]

    def get(self, request, *args, **kwargs):
        cart_id = request.session.get('cart_id')
        product_id = kwargs.get('product_id')
        quantity = kwargs.get('quantity')
        if product_id and quantity:
            CartItem.objects.create(cart_id=cart_id, product_id=product_id, item_qty=quantity)

        return HttpResponseRedirect(reverse('shop_home'))
