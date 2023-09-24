# Necessary imports:
# - `authenticate` from Django to verify user credentials.
# - `swagger_auto_schema` for generating Swagger docs for the API endpoint.
# - Various utilities from DRF for creating API views, returning responses, and handling exceptions.
# - `LoginSerializer` for serializing and validating login data.
# - `Token` model from DRF for generating or fetching authentication tokens.

from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions
from account.serializers.authetificated import LoginSerializer
from rest_framework.authtoken.models import Token

class LoginHubView(APIView):
    """
    View to handle user login and return an authentication token.
    This view handles POST requests to authenticate users.
    """

    @swagger_auto_schema(
        operation_summary='do not required for front'
    )
    def post(self, request, *args, **kwargs):
        """
        Handle POST request for user authentication.
        
        Args:
            request (HttpRequest): Request object encapsulating the POST data.
        
        Returns:
            Response: JSON response containing the authentication token and user details.
        """
        # Serialize and validate the request data using the LoginSerializer.
        serializer = LoginSerializer(data=request.data)
        
        # Ensure data is valid, if not, a validation exception will be raised.
        serializer.is_valid(raise_exception=True)

        # Use Django's `authenticate` method to verify the user's credentials.
        user = authenticate(username=serializer.validated_data['username'], 
                            password=serializer.validated_data['password'])

        # If the credentials are invalid (i.e., `user` is None), raise an authentication exception.
        if not user:
            raise exceptions.AuthenticationFailed(' “Логин или пароль введен неверно. Попробуйте снова.”')

        # Get or create an authentication token for the validated user.
        token, created = Token.objects.get_or_create(user=user)

        # Return a response containing the authentication token and relevant user details.
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.username,  # Assuming 'username' field stores email, otherwise consider changing the key.
            'is_superuser': user.is_superuser,
            'is_active': user.is_active,
        })
