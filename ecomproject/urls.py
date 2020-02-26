from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import index
from accounts.views import login_page, logout_page, guest_register_page
from addresses.views import checkout_address_create_view, checkout_address_reuse_view
from contacts.views import contactView
from django.views.generic import TemplateView

urlpatterns = [
	path('', index, name="home"),
	path('product/', include(('products.urls','products'))),
	path('search/', include(('search.urls','search'))),
	path('cart/', include(('cart.urls','cart'))),
    path('admin/', admin.site.urls),
	path('login/', login_page, name="login"),
	path('checkout/address/create/', checkout_address_create_view, name="checkout_address_create"),
	path('checkout/address/reuse/', checkout_address_reuse_view, name="checkout_address_reuse"),
	path('logout/', logout_page, name="logout"),
	path('register/guest/', guest_register_page, name="guest_register"),
	path('bootstrap/', TemplateView.as_view(template_name="bootstrap/example.html")),
	path('contact/', contactView, name="contact"),
]

urlpatterns = urlpatterns + static(settings.STATIC_URL)

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)