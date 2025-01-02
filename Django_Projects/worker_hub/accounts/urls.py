from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from .accounts_views import register, activate_account, activation_sent, custom_login


urlpatterns = [
    path('register/', register, name='register'),
    path('activation-sent/', activation_sent, name='activation_sent'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate'),
    # path('login/', LoginView.as_view(template_name='accounts/auth/login.html'), name='login'),
    path('login/', custom_login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_reset/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/reset_done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]