from django.urls import path

from .views import home_page_view, login_view, registration_view, registration_redirect, logout_view, signup, activate

urlpatterns = [
    path('', home_page_view, name='home'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('registration', registration_view, name='registration'),
    path('registration/redirect', registration_redirect, name='registration_redirect'),
    path('signup/', signup, name='signup'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
         activate, name='activate'),
]
