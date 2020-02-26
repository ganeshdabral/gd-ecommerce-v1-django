from django.utils.translation import ugettext_lazy as _
from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = (
            'firstname',
            'lastname',
            'address_line_1',
            'address_line_2',
            'city',
            'state',
            'postal_code',
            'phone',
            'country',
        )
        labels = {
            'firstname': _(''),
        }
        widgets = {
            'firstname': forms.TextInput(attrs={'placeholder': 'First Name', 'label':''}),
            'lastname': forms.TextInput(attrs={'placeholder': 'Last Name', 'label': ''}),
            'country': forms.Select(attrs={'class': 'cart-select country-usa', 'label': ''}),
        }

