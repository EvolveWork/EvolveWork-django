from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class Product(models.Model):
    id = models.CharField(max_length=255, blank=True, primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Plan(models.Model):
    id = models.CharField(max_length=255, blank=True, primary_key=True)
    currency = models.CharField(max_length=3,
                                blank=True, null=True)
    interval = models.CharField(max_length=255, default='Month', editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    amount = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nickname


class CustomUserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address.")
        if not full_name:
            raise ValueError("Please input your full name.")
        if not password:
            raise ValueError("Users must have a password.")

        user_obj = self.model(
            email=self.normalize_email(email),
            full_name=full_name
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.is_active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, full_name, password=None):
        user = self.create_user(
            email,
            full_name=full_name,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, email, full_name, password=None):
        user = self.create_user(
            email,
            full_name=full_name,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    # Address information gathered from Stripe subscribe form:
    stripeId = models.CharField(max_length=255, blank=True, null=True)
    stripeBillingAddressLine1 = models.CharField(max_length=255, blank=True, null=True)
    zipCode = models.CharField(max_length=255, blank=True, null=True)
    billingAddressState = models.CharField(max_length=255, blank=True, null=True)
    billingAddressCity = models.CharField(max_length=255, blank=True, null=True)
    billingAddressCountry = models.CharField(max_length=2, blank=True, null=True)

    # Stripe Subscription information:
    subscription_id = models.CharField(max_length=255, blank=True, null=True)
    renewal_date = models.CharField(max_length=255, blank=True, null=True)
    cancel_at_period_end = models.BooleanField(default=False, blank=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email

    def get_short_name(self):
        if ' ' in self.full_name:
            return self.full_name[:self.full_name.find(' ')]
        return self.email

    def set_stripe_id(self, stripe_id):
        self.stripeId = stripe_id

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def active(self):
        return self.is_active
