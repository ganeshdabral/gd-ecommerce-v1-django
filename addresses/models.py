from django.db import models
from billing.models import BillingProfile

ADDRESS_TYPES = (
    ('billing','Billing'),
    ('shipping','Shipping')
)

COUNTRY = (
    ('usa','USA'),
)

class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=50, choices=ADDRESS_TYPES)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    address_line_1 = models.CharField(max_length=120, null=True)
    address_line_2 = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    country = models.CharField(max_length=50, choices=COUNTRY, default='USA')

    def __str__(self):
        return str(self.billing_profile)