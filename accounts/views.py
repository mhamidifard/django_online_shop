from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import status, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from accounts.serilizers import UserRegistrationSerializer, UserProfileSerializer, UserLoginSerializer, \
    UserLogoutSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer


class TestAuthentication(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, format=None):
        return Response({'message': 'You are logged in'}, status=status.HTTP_200_OK)
class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_data=UserProfileSerializer(user).data
        refresh = RefreshToken.for_user(user)

        return Response({'message': 'User registered',
                         'user':user_data,
                         'refresh': str(refresh),
                         'access': str(refresh.access_token)},
                          status=status.HTTP_201_CREATED)
class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserLogoutView(APIView):
    serializer_class =UserLogoutSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data['refresh']

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return Response({"detail": "Invalid or already blacklisted token."},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
class PasswordResetRequestView(APIView):
    serializer_class = PasswordResetRequestSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # برای امنیت، پیام کلی
            return Response(
                {"detail": "If an account with this email exists, you will receive a password reset email.."},
                status=status.HTTP_200_OK
            )

        # Generate uid and token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # Construct reset link
        reset_link = f"https://your-frontend-domain.com/reset-password?uid={uid}&token={token}"

        # Send email (simplified)
        # send_mail(
        #     subject="Password Reset Request",
        #     message=f"Click the link below to reset your password:\n{reset_link}",
        #     from_email="no-reply@yourdomain.com",
        #     recipient_list=[user.email],
        #     fail_silently=False,
        # )
        print(f"uid: {uid}\ntoken: {token}")

        return Response(
            {"detail": "If an account with this email exists, you will receive a password reset email."},
            status=status.HTTP_200_OK
        )

class PasswordResetConfirmView(APIView):
    serializer_class = PasswordResetConfirmSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = serializer.validated_data['uid']
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']

        try:
            uid_decoded = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid_decoded)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            return Response({"detail": "Invalid UID."}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)