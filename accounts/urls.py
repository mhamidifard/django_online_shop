from django.urls import path

from accounts.views import (
    PasswordResetConfirmView,
    PasswordResetRequestView,
    TestAuthentication,
    UserLoginView,
    UserLogoutView,
    UserRegistrationView,
)

urlpatterns = [
    path('test-authentication/', TestAuthentication.as_view(), name='test-authentication'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]
