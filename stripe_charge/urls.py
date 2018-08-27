from django.urls import path

from .views import charge_view, checkout, charge_success, cancel_subscription

urlpatterns = [
    path('', charge_view, name='charge'),
    # path('register_and_checkout/', register_and_checkout, name='register_and_checkout'),
    path('cancel/', cancel_subscription, name='cancel_subscription'),
    path('checkout/', checkout, name="checkout"),
    path('success/', charge_success, name="charge_success"),
]
