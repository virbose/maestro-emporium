import factory
import factory.fuzzy
from shop.models import Cart, Product, CartItem

class CartFactory(factory.django.DjangoModelFactory):
    """
    Cart Factory
    """
    class Meta:
        model = Cart
    

class ProductFactory(factory.django.DjangoModelFactory):
    """
    Product Factory
    """
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f'Product #{n}')
    item_price = factory.fuzzy.FuzzyDecimal(low=1, high=1000, precision=2)


class CartItemFactory(factory.django.DjangoModelFactory):
    """
    Cart Item Factory
    """
    class Meta:
        model = CartItem

    cart = factory.SubFactory(CartFactory)
    product = factory.SubFactory(ProductFactory)
    item_qty = factory.fuzzy.FuzzyInteger(low=1, high=100)
