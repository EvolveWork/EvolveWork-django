from django.urls import path

from .views import charge_view, checkout, charge_success

urlpatterns = [
    path('', charge_view, name='charge'),
    path('checkout/', checkout, name="checkout"),
    path('success/', charge_success, name="charge_success")
]
