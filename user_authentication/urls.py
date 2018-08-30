from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views

from .views import home_page_view, signup, account, logout

urlpatterns = [
    path('', home_page_view, name='home'),
    path('signup/', signup, name='signup'),
    path('account/', account, name='account'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', logout, name='logout'),
    path('logout/success/', auth_views.LogoutView.as_view(), name='logout_success'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^password_reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete')
    # path('reset/<uidb64>/<token>/', auth_views.password_reset_confirm, name='password_reset_confirm'),
    # path('reset/done/', auth_views.password_reset_complete, name='password_reset_complete'),
]
