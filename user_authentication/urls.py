from django.conf.urls import url
from django.urls import path, include

from .views import home_page_view, signup, activate, signup_confirm

urlpatterns = [
    path('', home_page_view, name='home'),
    path('signup/', signup, name='signup'),
    path('signup/confirm', signup_confirm, name='signup_confirm'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
    path('accounts/', include('django.contrib.auth.urls')),
]
