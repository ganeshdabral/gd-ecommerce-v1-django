import math,decimal
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, m2m_changed

from products.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()
#User = settings.AUTH_USER_MODEL
class CartManager(models.Manager):


    def new_or_get(self,request):
        cart_id = request.session.get('cart_id', None)
        qs = self.model.objects.filter(id=cart_id, active=True)
        print(cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
            print('Cart ID Exists')
        else:
            cart_obj = Cart.objects.new(user=request.user)
            print(cart_obj.id)
            request.session['cart_id'] = cart_obj.id
            new_obj = True
            print('New Cart Created')
        return cart_obj, new_obj

    def new(self,user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
                qs = self.model.objects.filter(user=user_obj.id, active=True)
                if qs.count() >= 1:
                    return qs.first()
        return self.model.objects.create(user=user_obj)

class Cart(models.Model):
    user        =   models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    products    =   models.ManyToManyField(Product,blank=True)
    subtotal    =   models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    total       =   models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    active      =   models.BooleanField(default=True)
    update_ts   =   models.DateTimeField(auto_now=True)
    create_ts   =   models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)

def m2m_changed_cart_reciver(sender, instance, action, *args, **kwargs):
    print(action)
    print(instance.products)
    print(instance.total)
    if action == "post_add" or action == "post_remove" or action == "post_clear":
        total = 0
        products = instance.products.all()
        for product_obj in products:
            total += product_obj.price
        instance.subtotal = total
        instance.save()

m2m_changed.connect(m2m_changed_cart_reciver, sender=Cart.products.through)

def pre_save_cart_reciver(sender, instance, *args, **kwargs):
    if instance.subtotal > 0:
        tax = instance.subtotal * decimal.Decimal((2/100))
        instance.total = math.fsum([instance.subtotal, tax])
    else:
        instance.total = 0

pre_save.connect(pre_save_cart_reciver, sender=Cart)