from django.contrib.auth import views as auth_views
from django.urls import path

from .views import home_page_view, signup, account, logout

urlpatterns = [
    path('', home_page_view, name='home'),
    path('signup/', signup, name='signup'),
    path('account/', account, name='account'),
    path('login/', auth_views.login, name='login'),
    path('logout/', logout, name='logout'),
    path('logout/success/', auth_views.logout, name='logout_success'),
    path('password_change/', auth_views.password_change, name='password_change'),
    path('password_change/done/', auth_views.password_change_done, name='password_change_done'),
    # path('password_reset/', auth_views.password_reset, name='password_reset'),
    # path('password_reset/done/', auth_views.password_reset_done, name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.password_reset_confirm, name='password_reset_confirm'),
    # path('reset/done/', auth_views.password_reset_complete, name='password_reset_complete'),
]
