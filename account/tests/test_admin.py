from django.test import TestCase
from account.tests.factories import MyUserFactory
from account.models import MyUser
from account.admin import ModelAdmin  # Import the ModelAdmin class from the account.admin module

class ModelAdminTests(TestCase):

    def setUp(self):
        self.user = MyUserFactory()
        self.site = AdminSite()

    def test_modeladmin_str(self):
        ma = ModelAdmin(MyUser, self.site)  # Create a ModelAdmin instance for the MyUser model
        self.assertEqual(str(ma), 'account.ModelAdmin')  # Check that the string representation of the ModelAdmin is as expected

    def test_default_attributes(self):
        ma = ModelAdmin(MyUser, self.site)  # Create a ModelAdmin instance for the MyUser model
        self.assertEqual(ma.actions, ())  # Check that the actions attribute is an empty tuple
        self.assertEqual(ma.inlines, ())  # Check that the inlines attribute is an empty tuple
