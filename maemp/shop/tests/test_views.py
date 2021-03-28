from django.test import TestCase
from django.apps import apps
from django.urls import reverse


class ShopHomeViewTest(TestCase):
    fixtures = ['products']

    def setUp(self) -> None:
        self.url = reverse('shop_home')

    def test_home_page_ok(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_home_page_no_post(self) -> None:
        response = self.client.post(self.url, {'data': 'some-invalid-post-data'})
        self.assertEqual(response.status_code, 405)


class AddItemToCartViewTest(TestCase):
    fixtures = ['products']

    def setUp(self) -> None:
        Product = apps.get_model('shop', 'Product')
        self.product = Product.objects.first()
        self.quantity = 5
        self.url = reverse('add_to_cart', kwargs={
            'product_id': self.product.pk,
            'quantity': self.quantity
        })
        self.redirect_url = reverse('shop_home')

    def test_add_to_cart_ok(self) -> None:
        CartItem = apps.get_model('shop', 'CartItem')
        self.client.get(self.url)
        self.assertEqual(CartItem.objects.filter(product_id=self.product.pk).count(), 1)

    def test_add_to_cart_redirect(self) -> None:
        response = self.client.get(self.url)
        self.assertRedirects(response, self.redirect_url)

    def test_add_to_cart_again(self) -> None:
        CartItem = apps.get_model('shop', 'CartItem')
        # Call once
        self.client.get(self.url)
        ci_len = CartItem.objects.filter(product_id=self.product.pk).count()
        # Call again
        self.client.get(self.url)
        # ensure there is still the same number of cartItems
        self.assertEqual(ci_len, CartItem.objects.filter(product_id=self.product.pk).count())

    def test_add_to_cart_no_post(self) -> None:
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)

    def test_add_to_cart_bad_qty(self) -> None:
        url = reverse('add_to_cart', kwargs={
            'product_id': self.product.pk,
            'quantity': 'bad_qty'
        })
        with self.assertRaises(ValueError):
            self.client.get(url)

    def test_add_to_cart_bad_product(self) -> None:
        url = reverse('add_to_cart', kwargs={
            'product_id': 'bad_pk',
            'quantity': self.quantity
        })
        with self.assertRaises(ValueError):
            self.client.get(url)
