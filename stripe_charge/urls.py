from django.urls import path

from .views import charge_view, checkout, charge_success, cancel_subscription, cancel_subscription_complete
# renew_subscription, renew_subscription_complete

urlpatterns = [
    path('', charge_view, name='charge'),
    path('checkout/', checkout, name="checkout"),
    path('success/', charge_success, name="charge_success"),
    path('cancel/', cancel_subscription, name='cancel_subscription'),
    path('cancel/complete/', cancel_subscription_complete, name='cancel_subscription_complete'),
    # path('renew/', renew_subscription, name='renew_subscription'),
    # path('renew/complete/', renew_subscription_complete, name='renew_subscription_complete')
    # path('register_and_checkout/', register_and_checkout, name='register_and_checkout'),
]
