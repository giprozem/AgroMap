import json

# Required imports for Django and Django Rest Framework
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

# Import the required model
from account.models.account import MyUser


class AuthenticatedViewTestCase(APITestCase):
    
    # URL endpoint that will be tested
    _URL_ = "/hub/login_hub/"

    # Setup method to prepare the test environment
    # This is executed before each individual test method in this class
    def setUp(self) -> None:
        # Create a user instance for the test
        user = MyUser(username="test_username", is_active=True)
        user.set_password("test_password")
        user.save()
        self.user = user  # Assign the created user instance to the class variable

    # Helper method to prepare request content for the authentication process
    def _set_request_content(self) -> dict:
        data = {
            "username": "test_username",
            "password": "test_password",
        }
        return data

    # Test method to ensure a POST request to the login endpoint returns a 200 status code when provided valid credentials
    def test_authenticate_view_status_code(self):
        request_body = self._set_request_content()
        response = self.client.post(self._URL_, request_body)
        self.assertEqual(response.status_code, 200)

    # Test method to check if the response content from the authentication endpoint matches expected data
    def test_authenticate_view_response_content(self):
        # Generate or fetch a token for the user
        token, created = Token.objects.get_or_create(user=self.user)
        
        # Set the expected response content
        response_content = {
            "token": token.key,
            "user_id": self.user.pk,
            "email": self.user.username,  # Note: It's better to use self.user.email if the model has an email attribute
            "is_superuser": self.user.is_superuser,
            "is_active": self.user.is_active,
        }
        
        request_body = self._set_request_content()
        response = self.client.post(self._URL_, request_body)
        
        # Assert that the expected response matches the actual response data
        self.assertEqual(response_content, response.data)

    # Test method to check if the authentication process fails with an invalid password
    def test_authentication_failed(self):
        request_body = {"username": "test_username", "password": "invalid_password"}
        response = self.client.post(self._URL_, request_body)
        # A 401 status code indicates unauthorized access
        self.assertEqual(response.status_code, 401)
