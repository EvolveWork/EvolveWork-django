from django.db import models


class BillingProfile(models.Model):
    email = models.EmailField(max_length=50)
    name = models.CharField(max_length=255)
    stripeId = models.CharField(max_length=255)
    stripeBillingAddressLine1 = models.CharField(max_length=255)
    zipCode = models.CharField(max_length=255, default=None)
    billingAddressState = models.CharField(max_length=255, default=None)
    billingAddressCity = models.CharField(max_length=255, default=None)
    billingAddressCountry = models.CharField(max_length=255, default=None)
