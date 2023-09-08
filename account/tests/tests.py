from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from rest_framework.test import APITestCase
from account.tests.factories import MyUserFactory, TokenFactory, AdminUserFactory


class TestUser(APITestCase):

    def test_login_api(self):
        self.user = MyUserFactory()
        request_body = {
            "username": self.user.username,
            "password": self.user.password
        }
        response = self.client.post("/account/login_agromap/", request_body, format="json")
        self.assertEqual(response.status_code, 401)

    def test_login(self):
        password = 'test_1_password'
        self.user = MyUserFactory(password=password)
        self.assertTrue(self.client.login(username=self.user.username, password=password))

    def test_invalid_login(self):
        password = "invalid_password"
        self.user = MyUserFactory()
        self.assertFalse(self.client.login(username=self.user.username, password=password))

    def test_invalid_username(self):
        username = "invalid_username"
        self.user = MyUserFactory(username=username)
        self.assertFalse(self.client.login(username=username, password=self.user.password))

    def test_profile(self):
        self.token = TokenFactory()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/account/get_profile/')
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_edit_profile(self):
        self.token = TokenFactory()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.patch('/account/edit_profile/', {'full_name': 'test_user', "phone_number": "+996700000000"})
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_change_password(self):
        self.token = TokenFactory()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post('/account/change_password/',
                                    {'old_password': 'test_1_password',
                                     'password': 'test_2_password',
                                     'password_confirm': 'test_2_password'})
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_logout(self):
        self.token = TokenFactory()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/account/logout_agromap/')
        self.assertEqual(response.status_code, HTTP_200_OK)
        response = self.client.get('/account/get_profile/')
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_notification(self):
        self.token = TokenFactory()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/account/notifications/')
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_read_notification(self):
        self.token = TokenFactory()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.patch(f'/account/notifications/1/')
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_admin(self):
        password = 'admin_password'
        self.user = AdminUserFactory(password=password)
        self.assertTrue(self.client.login(username=self.user.username, password=password))
        self.assertTrue(self.user.is_staff)
