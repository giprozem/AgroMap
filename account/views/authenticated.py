from django.contrib.auth import authenticate
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions
from account.serializers.authetificated import LoginSerializer, ProfileSerializer, ChangePasswordSerializer, \
    NotificationsSerializer
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _
from account.models.account import Profile
from rest_framework.generics import GenericAPIView
from rest_framework.generics import ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from account.models.account import Notifications


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
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])

        if not user:
            raise exceptions.AuthenticationFailed(_('“Логин или пароль введен неверно. Попробуйте снова.”'))

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'is_superuser': user.is_superuser,
            'is_active': user.is_active,
        })


class UpdateProfileAPIView(GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        instance = Profile.objects.get(my_user=self.request.user)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ChangePasswordAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
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


class GetProfileAPIView(GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = Profile.objects.get(my_user=request.user)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


class NotificationsAPIView(ListAPIView):
    serializer_class = NotificationsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = Notifications.objects.filter(user=user, is_read=False)
        return queryset


class ReadNotificationAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request, pk):
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
                "en": "Token wasnot found"
            }
        return Response({"message": message})


class LogoutAgromapView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        Token.objects.get(user=request.user).delete()
        return Response("Token is deleted")
