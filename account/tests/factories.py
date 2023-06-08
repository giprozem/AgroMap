from factory.django import DjangoModelFactory
from factory import SubFactory, PostGenerationMethodCall, RelatedFactory, Iterator
from faker import Faker
from account.models.account import MyUser, Profile, Notifications
from rest_framework.authtoken.models import Token


class MyUserFactory(DjangoModelFactory):
    class Meta:
        model = MyUser

    username = 'test_1_user'
    password = PostGenerationMethodCall('set_password', 'test_1_password')
    profiles = RelatedFactory('account.tests.factories.ProfileFactory', factory_related_name='my_user')


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile

    my_user = SubFactory(MyUserFactory, profiles=None)
    full_name = Faker().name()
    phone_number = Faker().pystr(max_chars=12)


class NotificationsFactory(DjangoModelFactory):
    class Meta:
        model = Notifications

    user = SubFactory(MyUserFactory)
    date = Faker().date_time()
    text = Faker().pystr(max_chars=75)


class TokenFactory(DjangoModelFactory):
    class Meta:
        model = Token

    user = SubFactory(MyUserFactory)
