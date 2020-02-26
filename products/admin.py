from django.contrib import admin
from .models import Product
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','__str__','slug','price']

admin.site.register(Product,ProductAdmin)