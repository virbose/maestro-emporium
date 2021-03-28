from django.utils.deprecation import MiddlewareMixin

from shop.models import Cart


class CartMiddleware(MiddlewareMixin):
    def process_request(self, request):
        assert hasattr(request, 'session'), (
            "The Cart middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'shop.middleware.CartMiddleware'."
        )
        if 'cart_id' not in request.session:
            request.session['cart_id'] = Cart.objects.create().pk