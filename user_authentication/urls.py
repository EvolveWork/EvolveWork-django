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
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/confirm/', auth_views.PasswordResetConfirmView.as_view(), name='password_resert_confirm'),
    # path('reset/<uidb64>/<token>/', auth_views.password_reset_confirm, name='password_reset_confirm'),
    # path('reset/done/', auth_views.password_reset_complete, name='password_reset_complete'),
]
