from django.urls import path

import accounts
from accounts.views import UserRegistrationView, TestAuthentication

urlpatterns = [
    path('test-authentication/', TestAuthentication.as_view(), name='test-authentication'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('register/', accounts.views.UserRegistrationView.as_view(), name='user-register'),
    path('login/', accounts.views.UserLoginView.as_view(), name='user-login'),
    path('logout/', accounts.views.UserLogoutView.as_view(), name='user-logout'),
    path('password-reset/', accounts.views.PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/confirm/', accounts.views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]