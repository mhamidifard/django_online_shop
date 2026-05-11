import logging
from urllib.parse import quote

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema, extend_schema_view, inline_serializer
from rest_framework import serializers

from accounts.models import User
from accounts.serilizers import UserRegistrationSerializer, UserProfileSerializer, UserLoginSerializer, \
    UserLogoutSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer
from accounts.tasks import send_password_reset_email, send_welcome_email

logger = logging.getLogger(__name__)


@extend_schema_view(
    get=extend_schema(
        tags=["accounts"],
        description="Validate the current JWT access token and return authentication state.",
        responses=inline_serializer(
            name="AuthCheckResponse",
            fields={"message": serializers.CharField()},
        ),
    )
)
class TestAuthentication(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, format=None):
        return Response({'message': 'You are logged in'}, status=status.HTTP_200_OK)


@extend_schema_view(
    post=extend_schema(
        tags=["accounts"],
        description="Register a new user and return profile plus JWT token pair.",
        request=UserRegistrationSerializer,
    )
)
class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_data=UserProfileSerializer(user).data
        refresh = RefreshToken.for_user(user)

        # Send welcome email asynchronously
        try:
            send_welcome_email.apply_async(
                args=[user.email, user.get_full_name() or user.email],
                queue='default',
                priority=5
            )
        except Exception:
            logger.exception("Failed to queue welcome email for user_id=%s", user.id)

        return Response({'message': 'User registered',
                         'user':user_data,
                         'refresh': str(refresh),
                         'access': str(refresh.access_token)},
                          status=status.HTTP_201_CREATED)


@extend_schema_view(
    post=extend_schema(
        tags=["accounts"],
        description="Authenticate user credentials and return JWT tokens.",
        request=UserLoginSerializer,
    )
)
class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema_view(
    post=extend_schema(
        tags=["accounts"],
        description="Blacklist a refresh token and log out the current user.",
        request=UserLogoutSerializer,
    )
)
class UserLogoutView(APIView):
    serializer_class =UserLogoutSerializer
    permission_classes = [IsAuthenticated]

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


@extend_schema_view(
    post=extend_schema(
        tags=["accounts"],
        description="Request a password reset link by email (rate limited).",
        request=PasswordResetRequestSerializer,
    )
)
class PasswordResetRequestView(APIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "password_reset"

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.filter(email=email).first()
        success_message = {"detail": "If an account with this email exists, you will receive a password reset email."}
        if not user:
            return Response(success_message, status=status.HTTP_200_OK)

        # Generate uid and token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # Construct reset link compatible with frontend route and backend confirm contract.
        frontend_base = settings.FRONTEND_URL.rstrip("/")
        confirm_path = settings.PASSWORD_RESET_CONFIRM_PATH
        if not str(confirm_path).startswith("/"):
            confirm_path = f"/{confirm_path}"
        encoded_uid = quote(uid, safe="")
        encoded_token = quote(token, safe="")
        reset_link = f"{frontend_base}{confirm_path}/?uid={encoded_uid}&token={encoded_token}"

        # Send password reset email asynchronously
        try:
            send_password_reset_email.apply_async(
                args=[user.email, reset_link],
                queue='critical',
                priority=10
            )
        except Exception:
            logger.exception("Failed to queue password reset email for user_id=%s", user.id)

        return Response(success_message, status=status.HTTP_200_OK)


@extend_schema_view(
    post=extend_schema(
        tags=["accounts"],
        description="Reset password using `uid`, `token`, and a new password.",
        request=PasswordResetConfirmSerializer,
    )
)
class PasswordResetConfirmView(APIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [AllowAny]

    @staticmethod
    def _get_user_from_uid(uid):
        try:
            uid_decoded = urlsafe_base64_decode(uid).decode()
            return User.objects.get(pk=uid_decoded)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            return None

    @staticmethod
    def _is_valid_reset_token(user, token):
        return bool(user and default_token_generator.check_token(user, token))

    def post(self, request):
        payload = request.data.copy()
        if not payload.get("uid"):
            payload["uid"] = request.query_params.get("uid")
        if not payload.get("token"):
            payload["token"] = request.query_params.get("token")

        serializer = self.serializer_class(data=payload)
        serializer.is_valid(raise_exception=True)

        uid = serializer.validated_data['uid']
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']
        user = self._get_user_from_uid(uid)
        if not user:
            return Response({"detail": "Invalid uid."}, status=status.HTTP_400_BAD_REQUEST)
        if not self._is_valid_reset_token(user, token):
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save(update_fields=["password"])

        return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)

    def get(self, request):
        uid = request.query_params.get("uid")
        token = request.query_params.get("token")
        print(token)
        if not uid or not token:
            return Response({"detail": "uid and token are required."}, status=status.HTTP_400_BAD_REQUEST)
        user = self._get_user_from_uid(uid)
        if not user:
            return Response({"detail": "Invalid uid."}, status=status.HTTP_400_BAD_REQUEST)
        if not self._is_valid_reset_token(user, token):
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Token is valid."}, status=status.HTTP_200_OK)
