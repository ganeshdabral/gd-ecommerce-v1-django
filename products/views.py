from django.http import Http404
from django.views.generic import ListView, DetailView
from django.shortcuts import render
from .models import Product
from cart.models import Cart
# Create your views here.

class ProductListView(ListView):
	queryset = Product.objects.all()
	template_name = "products/list.html"

	def get_context_data(self, *args, **kwargs):
		context = super(ProductListView, self).get_context_data(*args,*kwargs)
		cart_obj, new_obj = Cart.objects.new_or_get(self.request)
		context['cart'] = cart_obj
		return context

class ProductDetailView(DetailView):
	#queryset = Product.objects.all()
	template_name = "products/detail.html"
	# def get_object(self,*args,**kwargs):
	# 	pk = self.kwargs.get('pk')
	# 	instance = Product.objects.get_by_id(pk)
	# 	print(instance)
	# 	if instance is None:
	# 		raise Http404("product not found")
	# 	return instance
	def get_queryset(self,*args,**kwargs):
		request = self.request
		pk = self.kwargs.get('pk')
		qs = Product.objects.filter(pk=pk)
		if qs.count() == 1:
			return qs.first()
		raise Http404("product not found")

class ProductDetailSlugView(DetailView):
	queryset = Product.objects.all()
	template_name = "products/detail.html"

	def get_object(self, *args, **kwargs):
		request = self.request
		slug = self.kwargs.get('slug')
		try:
			instance = Product.objects.get(slug=slug)
		except Product.DoesNotExist:
			raise Http404("hmm product not exist yet")
		return instance

class ProductCategoryListView(ListView):
	template_name = "products/list.html"

	def get_queryset(self, *args, **kwargs):
		category = self.kwargs.get('category')
		return Product.objects.get_category(category)

class ProductFeatureListView(ListView):
	template_name = "products/list.html"

	def get_queryset(self):
		request = self.request
		return Product.objects.featured


class ProductFeatureDetailView(DetailView):
	template_name = "products/detail.html"

	def get_queryset(self):
		request = self.request
		return Product.objects.featured