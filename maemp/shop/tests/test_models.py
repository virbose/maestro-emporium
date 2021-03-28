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

    def test_cart_total_tax_empty(self) -> None:
        self.assertEqual(self.new_cart.cart_tax, 0)

    def test_cart_grand_total_empty(self) -> None:
        self.assertEqual(self.new_cart.cart_grand_total, 0)


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
    Note: This is testing a very special use case, therefore these tests are checking against fixed values.
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


class CartItemModelTestsStep2(TestCase):
    """
    CartItem model test specific to EqualExperts technical exercise step 2
    Note: This is testing a very special use case, therefore these tests are checking against fixed values. One would
    NEVER do unit tests this way.
    """

    def setUp(self) -> None:
        self.product = ProductFactory.create(
            name='Dove Soap',
            item_price=39.99
        )
        self.cartitem = CartItemFactory.create(
            product=self.product,
            item_qty=8
        )
        self.cart = self.cartitem.cart
        self.qty = self.cartitem.item_qty

    def test_repr(self) -> None:
        self.assertEqual(str(self.cartitem), 'Dove Soap - 8')

    def test_total(self) -> None:
        self.assertEqual(self.cart.cart_total, Decimal('319.92'))

    def test_items_in_cart(self) -> None:
        self.assertEqual(self.cart.items_in_cart, 8)

    def test_add_same_item_raises_exception(self) -> None:
        """
        We should not be able to add a new cart item for the same product, the view should always update existing ones
        """
        with self.assertRaises(IntegrityError):
            CartItemFactory.create(
                cart=self.cart,
                product=self.product,
                item_qty=6
            )


class CartItemModelTestsStep3(TestCase):
    """
    CartItem model test specific to EqualExperts technical exercise step 3
    Note: This is testing a very special use case, therefore these tests are checking against fixed values. One would
    NEVER do unit tests this way.
    """

    def setUp(self) -> None:
        qty=2
        self.product_1 = ProductFactory.create(
            name='Dove Soap',
            item_price=39.99
        )
        self.cartitem_1 = CartItemFactory.create(
            product=self.product_1,
            item_qty=qty
        )
        self.cart = self.cartitem_1.cart
        self.product_2 = ProductFactory.create(
            name='Axe Deo',
            item_price=99.99
        )
        self.cartitem_2 = CartItemFactory.create(
            cart=self.cart,
            product=self.product_2,
            item_qty=qty
        )

    def test_repr_item_1(self) -> None:
        self.assertEqual(str(self.cartitem_1), f'Dove Soap - 2')

    def test_repr_item_2(self) -> None:
            self.assertEqual(str(self.cartitem_2), 'Axe Deo - 2')

    def test_total_no_tax(self) -> None:
        self.assertEqual(self.cart.cart_total, Decimal('279.96'))

    def test_tax(self) -> None:
        self.assertEqual(self.cart.cart_tax, 35)

    def test_grand_total(self) -> None:
        self.assertEqual(self.cart.cart_grand_total, Decimal('314.96'))

    def test_items_in_cart(self) -> None:
        self.assertEqual(self.cart.items_in_cart, 4)

    def test_add_same_item_raises_exception(self) -> None:
        """
        We should not be able to add a new cart item for the same product, the view should always update existing ones
        """
        with self.assertRaises(IntegrityError):
            CartItemFactory.create(
                cart=self.cart,
                product=self.product_1,
                item_qty=6
            )
