from django.db import models


# Create your models here.
class BillingProfile(models.Model):
    email = models.EmailField(max_length=50)
    stripe_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    stripeBillingAddressLine1 = models.CharField(max_length=255)
    zipCode = models.CharField(max_length=255, default=None)
    billingAddressState = models.CharField(max_length=255, default=None)
    billingAddressCity = models.CharField(max_length=255, default=None)
    billingAddressCountry = models.CharField(max_length=255, default=None)
