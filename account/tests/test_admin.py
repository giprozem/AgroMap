from datetime import date

from django import forms
from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry
from django.contrib.admin.options import (
    HORIZONTAL,
    VERTICAL,
    ModelAdmin,
    TabularInline,
    get_content_type_for_model,
)
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.widgets import (
    AdminDateWidget,
    AdminRadioSelect,
    AutocompleteSelect,
    AutocompleteSelectMultiple,
)
from django.contrib.auth.models import User
from django.db import models
from django.forms.widgets import Select
from django.test import RequestFactory, SimpleTestCase, TestCase

from account.tests.factories import MyUserFactory
from account.models import MyUser
from account.admin import *


class ModelAdminTests(TestCase):

    def setUp(self):
        self.user = MyUserFactory()
        self.site = AdminSite()

    def test_modeladmin_str(self):
        ma = ModelAdmin(MyUser, self.site)
        self.assertEqual(str(ma), 'account.ModelAdmin')

    def test_default_attributes(self):
        ma = ModelAdmin(MyUser, self.site)
        self.assertEqual(ma.actions, ())
        self.assertEqual(ma.inlines, ())