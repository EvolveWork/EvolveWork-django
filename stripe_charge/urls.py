from django.urls import path

from .views import charge_view, checkout

urlpatterns = [
    path('', charge_view, name='charge'),
    path('checkout', checkout, name="checkout")
]
