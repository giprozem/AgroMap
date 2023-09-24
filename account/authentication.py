from account.models.account import MyUser
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from auditlog.middleware import AuditlogMiddleware
from auditlog.context import set_actor
from contextvars import ContextVar
from typing import Optional
from django.conf import settings
from django.http import HttpRequest
from django.utils import timezone

class MyTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        if not token.user.is_active:
            raise AuthenticationFailed('User not active or deleted.')

        # Update the last login timestamp for the user associated with the token.
        MyUser.objects.filter(username=token.user).update(last_login=timezone.now())
        return (token.user, token)

class AdminLastVisitMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # If the user is authenticated, update their last login timestamp.
        if request.user.is_authenticated:
            MyUser.objects.filter(pk=request.user.pk).update(last_login=timezone.now())
        response = self.get_response(request)
        return response

def set_cid(request: Optional[HttpRequest] = None) -> None:
    correlation_id = ContextVar("auditlog_correlation_id", default=None)
    cid = None
    header = ''

    if header and request:
        # Check if the header is present in the request and retrieve the correlation ID.
        if header in request.headers:
            cid = request.headers.get(header)
        elif header in request.META:
            cid = request.META.get(header)
    correlation_id.set(cid)

class MyAuditMiddleware(AuditlogMiddleware):
    @staticmethod
    def _get_actor(request):
        try:
            key = request.META.get('HTTP_AUTHORIZATION')
            token = Token.objects.get(key=key[6:])
            if token:
                return token.user
        except:
            return None

    def __call__(self, request):
        remote_addr = self._get_remote_addr(request)
        user = self._get_actor(request)

        # Set the correlation ID based on the request.
        set_cid(request)

        # Set the actor and remote address for audit logging.
        with set_actor(actor=user, remote_addr=remote_addr):
            return self.get_response(request)
