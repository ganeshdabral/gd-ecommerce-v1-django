from django.urls import path, re_path

from .views import ProductListView, ProductDetailSlugView, ProductCategoryListView

urlpatterns = [
	path('', ProductListView.as_view(), name="list"),
	path('<slug>', ProductDetailSlugView.as_view(), name="detail"),
	path('shop/<category>', ProductCategoryListView.as_view(), name="category"),
]
