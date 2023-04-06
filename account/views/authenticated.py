from django.contrib.auth import authenticate
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions
from account.serializers.authetificated import LoginSerializer, ProfileSerializer, ChangePasswordSerializer
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _
from account.models.account import Profile, MyUser
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


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


class UpdateProfileAPIView(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'my_user'
    permission_classes = (IsAuthenticated,)


class ChangePasswordAPIView(generics.UpdateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)


class GetProfileAPIView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'my_user'
    permission_classes = (IsAuthenticated,)
