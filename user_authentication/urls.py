from django.conf.urls import url
from django.urls import path, include

from .views import home_page_view, signup, activate, signup_confirm

urlpatterns = [
    path('', home_page_view, name='home'),

    path('accounts/', include('django.contrib.auth.urls')),
    # accounts/ login/ [name='login']
    # accounts/ logout/ [name='logout']
    # accounts/ password_change/ [name='password_change']
    # accounts/ password_change/done/ [name='password_change_done']
    # accounts/ password_reset/ [name='password_reset']
    # accounts/ password_reset/done/ [name='password_reset_done']
    # accounts/ reset/<uidb64>/<token>/ [name='password_reset_confirm']
    # accounts/ reset/done/ [name='password_reset_complete']
    path('signup/', signup, name='signup'),
    path('signup/confirm', signup_confirm, name='signup_confirm'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
]
