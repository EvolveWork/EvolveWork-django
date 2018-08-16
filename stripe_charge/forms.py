from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import ModelForm

from .models import BillingProfile


class StripeBillingForm(ModelForm):
    class Meta:
        model = BillingProfile
        fields = ('first_name', 'last_name', 'email', 'stripe_id')

    def add_error(self, message):
        self.errors[NON_FIELD_ERRORS] = self.error_class([message])
