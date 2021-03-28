from django.urls import path
from shop.views import ShopHomeView, AddToCartView

urlpatterns = [
    path('add-to-cart/<product_id>/<quantity>', AddToCartView.as_view(), name="add_to_cart"),
    path('', ShopHomeView.as_view(), name="shop_home"),
]