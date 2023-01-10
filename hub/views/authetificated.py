from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions
from hub.serializers.authetificated import LoginSerializer
from rest_framework.authtoken.models import Token


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
        print(user)
        if not user:
            raise exceptions.AuthenticationFailed(' “Логин или пароль введен неверно. Попробуйте снова.”')

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.username,
            'is_superuser': user.is_superuser,
            'is_active': user.is_active,
        })