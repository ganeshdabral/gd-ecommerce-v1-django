from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q
from products.models import Product


class SearchProductView(ListView):
    template_name = "products/list.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        query = request.GET.get('q')
        if query is not None:
            lookup = Q(title__icontains=query) | Q(description__icontains=query)
            return Product.objects.filter(lookup).distinct()
        return Product.objects.featured
