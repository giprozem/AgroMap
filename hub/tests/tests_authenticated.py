import json

from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from account.models.account import MyUser


class AuthenticatedViewTestCase(APITestCase):
    _URL_ = "/hub/login_hub/"

    def setUp(self) -> None:
        user = MyUser(username="test_username", is_active=True)
        user.set_password("test_password")
        user.save()
        self.user = user

    def _set_request_content(self) -> dict:
        data = {
            "username": "test_username",
            "password": "test_password",
        }
        return data

    def test_authenticate_view_status_code(self):
        request_body = self._set_request_content()
        response = self.client.post(self._URL_, request_body)
        self.assertEqual(response.status_code, 200)

    def test_authenticate_view_response_content(self):
        token, created = Token.objects.get_or_create(user=self.user)
        request_body = self._set_request_content()
        response_content = {
            "token": token.key,
            "user_id": self.user.pk,
            "email": self.user.username,
            "is_superuser": self.user.is_superuser,
            "is_active": self.user.is_active,
        }
        response = self.client.post(self._URL_, request_body)
        self.assertEqual(response_content, response.data)

    def test_authentication_failed(self):
        request_body = {"username": "test_username", "password": "invalid_password"}
        response = self.client.post(self._URL_, request_body)
        self.assertEqual(response.status_code, 401)
