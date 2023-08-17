from account.models.account import MyUser
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone


class MyTokenAuthentication(TokenAuthentication):

    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        if not token.user.is_active:
            raise AuthenticationFailed('User not active or deleted.')

        # Update the last_used timestamp
        MyUser.objects.filter(username=token.user).update(last_login=timezone.now())
        return (token.user, token)


class AdminLastVisitMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            MyUser.objects.filter(pk=request.user.pk).update(last_login=timezone.now())
        response = self.get_response(request)
        return response
