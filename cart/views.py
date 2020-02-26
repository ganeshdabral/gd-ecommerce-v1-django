import decimal
from django.shortcuts import render,redirect
from .models import Cart
from products.models import Product
from orders.models import Order
from accounts.forms import LoginForm, RegistrationForm, GestForm
from billing.models import BillingProfile
from addresses.forms import AddressForm
from addresses.models import Address

# Create your views here.
def cart_create(user=None):
    cart_obj = Cart.objects.create(user=None)
    return cart_obj

def cart_view(request):
    cart_obj, new_obj =  Cart.objects.new_or_get(request)
    tax_amt = decimal.Decimal(cart_obj.subtotal)*(decimal.Decimal(2/100))
    context = {"cart_obj": cart_obj, "product_obj": cart_obj.products.all(), "gst_amount": round(tax_amt,2)}
    request.session['cart_count'] = cart_obj.products.count()
    return render(request,"cart/cart_home.html",context)
    #return HttpResponse("Hii.")

def cart_update(request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect(product_obj.get_abslute_url())
        cart_obj,new_obj = Cart.objects.new_or_get(request)
        cart_obj.products.add(product_obj)
        request.session['cart_count'] = cart_obj.products.count()
    return redirect('cart:home')

def cart_remove(request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect(product_obj.get_abslute_url())
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        cart_obj.products.remove(product_obj)
        request.session['cart_count'] = cart_obj.products.count()
    return redirect('cart:home')

def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    shipping_address_qs = None
    billing_address_qs = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect('cart:home')
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    billing_address_id = request.session.get('billing_address_id')
    shipping_address_id = request.session.get('shipping_address_id')

    if billing_profile is not None:
        address_qs = Address.objects.filter(billing_profile=billing_profile)
        shipping_address_qs = address_qs.filter(address_type="shipping")
        billing_address_qs = address_qs.filter(address_type="billing")
        order_obj,order_obj_created = Order.objects.new_or_get(cart_obj,billing_profile)
        if billing_address_id is not None and shipping_address_id is not None:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            order_obj.save()
            del request.session['billing_address_id']
            del request.session['shipping_address_id']
        if request.method == "POST":
            is_done = order_obj.check_order()
            if is_done:
                del request.session['cart_id']
                request.session['cart_count'] = 0
                order_obj.complete_order()
                cart_obj.active = False
                cart_obj.save()
                return redirect("cart:success")
    context = {
        "object": order_obj,
        "obj_count": cart_obj.products.count(),
        "billing_profile": billing_profile,
        "form_login" : LoginForm(),
        "form_registration" : RegistrationForm(),
        "form_guest" : GestForm(),
        "shipping_address": AddressForm(prefix="shipping"),
        "billing_address": AddressForm(prefix="billing"),
        "saved_shipping_address": shipping_address_qs,
        "saved_billing_address": billing_address_qs,
    }
    return render(request, "cart/checkout.html", context)

def checkout_success(request):
    return render(request, "cart/success.html", {})