from decimal import Decimal

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from shop.factories import CartFactory, ProductFactory, CartItemFactory


class CartModelTests(TestCase):
    
    def setUp(self) -> None:
        self.new_cart = CartFactory.create()

    def test_repr(self) -> None:
        cart_created = self.new_cart.created.isoformat()
        self.assertEqual(str(self.new_cart), f'Cart Created on {cart_created}')

    def test_cart_empty(self) -> None:
        self.assertEqual(self.new_cart.items_in_cart, 0)

    def test_cart_total_empty(self) -> None:
        self.assertEqual(self.new_cart.cart_total, 0)


class ProductModelTests(TestCase):
    
    def setUp(self) -> None:
        self.price = 39.99
        self.name = 'Dove Soap'
        self.new_product = ProductFactory.create(
            name=self.name,
            item_price=self.price
        )

    def test_repr(self) -> None:
        self.assertEqual(str(self.new_product), f'{self.name} - £{self.price}')

    def test_bad_price(self) -> None:
        with self.assertRaises(ValidationError):
            ProductFactory.create(
                item_price='bad_price_type'
            )
    
    def test_no_name(self) -> None:
        with self.assertRaises(IntegrityError):
            ProductFactory.create(
                name=None
            )


class CartItemModelTests(TestCase):
    """
    Generic test of CartItem model
    """

    def setUp(self) -> None:
        self.cartitem = CartItemFactory.create()
        self.cart = self.cartitem.cart
        self.product = self.cartitem.product
        self.qty = self.cartitem.item_qty

    def test_repr(self) -> None:
        self.assertEqual(str(self.cartitem), f'{self.product.name} - {self.qty}')

    def test_total(self) -> None:
        cart_total = self.cart.cart_total
        cart_total_calculated = self.product.item_price * self.qty
        self.assertEqual(cart_total, cart_total_calculated)

    def test_items_in_cart(self) -> None:
        self.assertEqual(self.cart.items_in_cart, self.qty)


class CartItemModelTestsStep1(TestCase):
    """
    CartItem model test specific to EqualExperts technical exercise step 1
    Note: This is testing a very special use case, therefore these tests are checking against fixed values
    """

    def setUp(self) -> None:
        self.product = ProductFactory.create(
            name='Dove Soap',
            item_price=39.99
        )
        self.cartitem = CartItemFactory.create(
            product=self.product,
            item_qty=5
        )
        self.cart = self.cartitem.cart
        self.qty = self.cartitem.item_qty

    def test_repr(self) -> None:
        self.assertEqual(str(self.cartitem), 'Dove Soap - 5')

    def test_total(self) -> None:
        self.assertEqual(self.cart.cart_total, Decimal('199.95'))

    def test_items_in_cart(self) -> None:
        self.assertEqual(self.cart.items_in_cart, 5)
