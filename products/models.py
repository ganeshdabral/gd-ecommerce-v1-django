from django.db import models
from django.urls import reverse


class ProductManager(models.Manager):
    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def featured(self):
        return self.get_queryset().filter(feature=True)

    def get_category(self, category):
        return self.get_queryset().filter(category=category)


# Create your models here.
class Product(models.Model):
    CHOICE = (('men', 'men'), ('women', 'women'), ('kids', 'kids'))
    title = models.CharField(max_length=120)
    description = models.TextField()
    category = models.CharField(null=True, max_length=12, choices=CHOICE, default=CHOICE[1][1])
    price = models.DecimalField(decimal_places=2, max_digits=10)
    image = models.FileField(upload_to='products/static/img/', null=True, blank=True)
    feature = models.BooleanField(default=False)
    slug = models.SlugField(null=True, blank=True, unique=True)

    objects = ProductManager()

    def __str__(self):
        return self.title

    def get_abslute_url(self):
        #  return f"/product/{self.slug}"
        return reverse("products:detail", kwargs={"slug": self.slug})
