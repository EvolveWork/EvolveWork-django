from django.urls import path

from .views import home_page_view, login_view, charge_view, registration_view, registration_redirect, logout_view

urlpatterns = [
    path('', home_page_view, name='home'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('registration', registration_view, name='registration'),
    path('registration/redirect', registration_redirect, name='registration_redirect'),
]
