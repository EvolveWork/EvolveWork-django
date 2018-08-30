from django.urls import path

from .views import charge_view, checkout, charge_success, cancel_subscription, cancel_subscription_complete

urlpatterns = [
    path('', charge_view, name='charge'),
    # path('register_and_checkout/', register_and_checkout, name='register_and_checkout'),
    path('cancel/', cancel_subscription, name='cancel_subscription'),
    path('cancel/complete/', cancel_subscription_complete, name='cancel_subscription_complete'),
    path('checkout/', checkout, name="checkout"),
    path('success/', charge_success, name="charge_success"),
]
