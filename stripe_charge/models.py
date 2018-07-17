from django.db import models


# Create your models here.
class BillingProfile(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=50)
    stripe_id = models.CharField(max_length=255)
