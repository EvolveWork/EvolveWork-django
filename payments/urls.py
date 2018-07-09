from django.urls import path

from .views import home_page_view, login_view, charge_view, registration_view, registration_redirect

urlpatterns = [
    path('', home_page_view, name='home'),
    path('registration', registration_view, name='registration'),
    path('registration/redirect', registration_redirect, name='registration_redirect'),
    path('login', login_view, name='login'),
    path('charge', charge_view, name='charge')
]