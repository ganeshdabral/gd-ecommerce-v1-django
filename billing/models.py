from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from accounts.models import GuestEmail
User = settings.AUTH_USER_MODEL

class BillingProfileManager(models.Manager):
    def new_or_get(self,request):
        created = False
        obj = None
        user = request.user
        guest_user_id = request.session.get("guest_email_id", None)
        if user.is_authenticated:
            qs_obj = self.model.objects.filter(email=user.email)
            if qs_obj.count() == 1:
                qs_obj.update(user=user)
                obj = qs_obj.first()
                created = False
            else:
                obj, created = self.model.objects.get_or_create(user=user, email=user.email)
        elif guest_user_id is not None:
            guest_obj = GuestEmail.objects.get(id=guest_user_id)
            print("email: "+guest_obj.email)
            obj, created = self.model.objects.get_or_create(email=guest_obj.email)
        else:
            pass
        return obj, created


class BillingProfile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = BillingProfileManager()

    def __str__(self):
        return self.email


def user_created_reciver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)

post_save.connect(user_created_reciver, sender=User)