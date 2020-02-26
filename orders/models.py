import math
from django.db import models
from django.db.models.signals import pre_save, post_save
from ecomproject.util import unique_order_id_genrate
from cart.models import Cart
from billing.models import BillingProfile
from addresses.models import Address

ORDER_STATUS_CHOICES = (
    ('created','Created'),
    ('paid','Paid'),
    ('shipped','Shipped'),
    ('refunded','Refunded')
)
class OrderManager(models.Manager):
    def new_or_get(self,cart_obj,billing_profile):
        created = False
        qs = self.get_queryset().filter(cart=cart_obj, billing_profile=billing_profile, active=True, status='created')
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(cart=cart_obj, billing_profile=billing_profile)
            created = True
        return obj, created

class Order(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, null=True, blank=True, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(Address, related_name='shipping_address', on_delete=models.CASCADE, blank=True, null=True)
    billing_address = models.ForeignKey(Address, related_name='billing_address', on_delete=models.CASCADE, blank=True, null=True)
    order_id = models.CharField(blank=True, max_length=100)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, default='created', choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(max_digits=100, decimal_places=2, default=5.0)
    total = models.DecimalField(max_digits=100, decimal_places=2, default=0.0)
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.order_id

    objects = OrderManager()

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = math.fsum([cart_total,shipping_total])
        self.total = new_total
        self.save()
        return new_total

    def check_order(self):
        if self.billing_profile and self.billing_address and self.shipping_address and self.total>0:
            return True
        else:
            return False

    def complete_order(self):
        if self.check_order():
            self.status = 'paid'
            self.save()
        return self.status


def pre_save_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_genrate(instance)
    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)

pre_save.connect(pre_save_order_id,sender=Order)

def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()

post_save.connect(post_save_cart_total,sender=Cart)

def post_save_order_total(sender, instance, created, *args, **kwargs):
    if created:
        print("updating...first")
        instance.update_total()

post_save.connect(post_save_order_total,sender=Order)