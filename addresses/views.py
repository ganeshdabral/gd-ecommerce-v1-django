from django.shortcuts import render,redirect
from django.utils.http import is_safe_url
from .forms import AddressForm
from .models import Address
from billing.models import BillingProfile

def checkout_address_reuse_view(request):
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    request_url = next_ or next_post or '/'
    shipping_id = request.POST.get('shipping_address', None)
    billing_id = request.POST.get('billing_address', None)
    if request.method == "POST":
        if shipping_id is not None and billing_id is not None:
            billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
            shipping_qs = Address.objects.filter(billing_profile=billing_profile, id=shipping_id)
            billing_qs = Address.objects.filter(billing_profile=billing_profile, id=billing_id)
            if shipping_qs.exists():
                request.session['shipping_address_id'] = shipping_id
            if billing_qs.exists():
                request.session['billing_address_id'] = billing_id
            if is_safe_url(request_url, request.get_host()):
                return redirect(request_url)
            else:
                return redirect('cart:checkout')

    return redirect('cart:checkout')

def checkout_address_create_view(request):
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    request_url = next_ or next_post or '/'
    shipping_form = AddressForm(request.POST, prefix="shipping")
    billing_form = AddressForm(request.POST, prefix="billing")
    if shipping_form.is_valid():
        same_as_shipping = request.POST.get('same_as_shipping', False)
        if same_as_shipping == "on":
            same_as_shipping = True
        shipping_instance = shipping_form.save(commit=False)
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if billing_profile is not None:
            shipping_instance.billing_profile = billing_profile
            shipping_instance.address_type = 'shipping'#request.POST.get('address_type', 'shipping')
            shipping_instance.save()
            request.session['shipping_address_id'] = shipping_instance.id
        else:
            print("Error: billing not found")
            return redirect('cart:checkout')

        if same_as_shipping is True:
            billing_form = AddressForm(request.POST, prefix="shipping")

        if billing_form.is_valid():
            instance = billing_form.save(commit=False)
            if billing_profile is not None:
                instance.billing_profile = billing_profile
                instance.address_type = 'billing'#request.POST.get('address_type', 'shipping')
                instance.save()
                request.session['billing_address_id'] = instance.id
            else:
                print("Error: billing not found")
                return redirect('cart:checkout')
            if is_safe_url(request_url, request.get_host()):
                return redirect(request_url)
            else:
                return redirect('cart:checkout')

    return redirect('cart:checkout')
