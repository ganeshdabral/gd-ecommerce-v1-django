from django.urls import path

from .views import cart_view, cart_update, cart_remove, checkout_home, checkout_success

urlpatterns = [
	path('', cart_view, name="home"),
	path('update/', cart_update, name="update"),
	path('remove/', cart_remove, name="remove"),
	path('checkout/', checkout_home, name="checkout"),
	path('success/', checkout_success, name="success"),
]
