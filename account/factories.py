from factory.django import DjangoModelFactory
from factory import Faker, SubFactory
from account.models.account import MyUser, Profile, Notifications


class MyUserFactory(DjangoModelFactory):
    class Meta:
        model = MyUser

    username = 'test_1_user'


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile

    my_user = SubFactory(MyUserFactory)
    full_name = Faker().name()
    phone_number = Faker().phone_number()


class NotificationsFactory(DjangoModelFactory):
    user = SubFactory(MyUserFactory)
    date = Faker().date_time()
    text = Faker().lorem()
