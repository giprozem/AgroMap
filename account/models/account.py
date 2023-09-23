from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


# The MyUser model extends the built-in User model.
class MyUser(AbstractUser):

    """
    This custom user model is designed to handle user authentication and management in a Django project.
    It extends the built-in AbstractUser class to add additional fields that indicate the type of user,
    such as administrators, farmers, workers, and observers.
    """

    # is_staff, is_farmer, is_employee, and is_supervisor are Boolean fields that indicate the type of user.
    is_staff = models.BooleanField(default=False, verbose_name=_('Administrator'))
    is_farmer = models.BooleanField(default=False, verbose_name=_('Farmer'))
    is_employee = models.BooleanField(default=False, verbose_name=_('Worker'))
    is_supervisor = models.BooleanField(default=False, verbose_name=_('Observer'))
    first_name = None  # The first_name and last_name fields are not used in this model.
    last_name = None

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    # Return the username when the object is represented as a string.
    def __str__(self):
        return self.username


# The Profile model is linked to the MyUser model with a one-to-one relationship.
class Profile(models.Model):

    """
    The Profile model is designed to store additional information about users of the application. 
    It is linked to the MyUser model using a one-to-one relationship, 
    allowing each user to have a corresponding profile with details such as full name and phone number.
    """

    my_user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True, related_name='profiles',
                                   verbose_name=_('User'))
    full_name = models.CharField(max_length=55, verbose_name=_('Full name'))
    phone_number = models.CharField(max_length=14, verbose_name=_('Phone number'))

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    # Return the username of the related user when the object is represented as a string.
    def __str__(self):
        return self.my_user.username


# The Notifications model stores notifications for users.
class Notifications(models.Model):

    """
    The Notifications model is designed to store notifications for users. 
    It allows you to associate notifications with specific users and track whether a notification has been read or not.
    """
    
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='notification',
                             verbose_name=_('User'))
    date = models.DateTimeField(auto_now=True, verbose_name=_('Created date'))
    text = models.CharField(max_length=100, verbose_name=_('Notification text'))
    is_read = models.BooleanField(default=False, verbose_name=_('Read'))

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')

    # Return the notification text when the object is represented as a string.
    def __str__(self):
        return self.text
