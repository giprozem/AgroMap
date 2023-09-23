from django.contrib.auth import authenticate
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions
from account.serializers.authetificated import LoginSerializer, ProfileSerializer, ChangePasswordSerializer, NotificationsSerializer
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _
from account.models.account import Profile, Notifications, MyUser
from rest_framework.generics import GenericAPIView
from rest_framework.generics import ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

# API View for user login
class LoginAgromapView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type='object',
            properties={
                'username': openapi.Schema(type='string'),
                'password': openapi.Schema(type='string'),
            },
            required=['username', 'password']
        ),
        responses={
            200: openapi.Schema(
                type='object',
                properties={
                    'token': openapi.Schema(type='string'),
                    'user_id': openapi.Schema(type='integer'),
                    'username': openapi.Schema(type='string'),
                    'is_superuser': openapi.Schema(type='boolean'),
                    'is_active': openapi.Schema(type='boolean'),
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        # Validate user credentials
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])

        if not user:
            raise exceptions.AuthenticationFailed(_('“The login or password was entered incorrectly. Try again.”'))

        # Generate a token for the user
        token, created = Token.objects.get_or_create(user=user)
        MyUser.objects.filter(username=user).update(last_login=timezone.now())

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'is_superuser': user.is_superuser,
            'is_active': user.is_active,
        })

# Generic API View for updating user profile
class UpdateProfileAPIView(GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        # Update user profile
        instance = Profile.objects.get(my_user=self.request.user)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

# API View for changing user password
class ChangePasswordAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        # Change user password
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['password_confirm'])
        request.user.save()
        message = {
            "ru": "Пароль изменен",
            "ky": "Сырсөз өзгөртүлдү",
            "en": "Password was changed"
        }
        return Response({"message": message})

# Generic API View for getting user profile
class GetProfileAPIView(GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # Get user profile
        queryset = Profile.objects.get(my_user=request.user)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

# List API View for getting user notifications
class NotificationsAPIView(ListAPIView):
    serializer_class = NotificationsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # Get user notifications
        user = self.request.user
        queryset = Notifications.objects.filter(user=user, is_read=False)
        return queryset

# Generic API View for marking a notification as read
class ReadNotificationAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request, pk):
        # Mark a notification as read
        user = self.request.user
        try:
            notification = Notifications.objects.get(user=user, pk=pk)
            notification.is_read = True
            notification.save()
            message = {
                "ru": "Уведомление прочитано",
                "ky": "Билдирүү окулган",
                "en": "Notification was read"
            }
        except:
            message = {
                "ru": "Токен не найден",
                "ky": "Токен табылган жок",
                "en": "Token was not found"
            }
        return Response({"message": message})

# API View for user logout
class LogoutAgromapView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # Delete the user's authentication token
        Token.objects.get(user=request.user).delete()
        return Response("Token is deleted")
