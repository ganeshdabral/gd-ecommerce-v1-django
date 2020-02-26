from django.db import models

class Contact (models.Model):

    firstname = models.CharField(null=True,blank=True, max_length=50)
    lastname = models.CharField(null=True, blank=True, max_length=50)
    email = models.EmailField(null=True, blank=True)
    subject = models.CharField(max_length=100, null=True, blank=True)
    message = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.email