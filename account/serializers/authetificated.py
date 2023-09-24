from rest_framework import serializers
from account.models.account import Profile
from rest_framework.exceptions import ValidationError
from account.models.account import Notifications

class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        fields = ('username', 'password')

class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile.
    """
    class Meta:
        model = Profile
        fields = ('full_name', 'phone_number')

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing user password.
    """
    old_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """
        Validate old password and password confirmation.
        """
        if not self.context.get('request').user.check_password(attrs['old_password']):
            raise ValidationError({'old_password': 'Wrong old password'})
        if attrs['password'] != attrs['password_confirm']:
            raise ValidationError({'password_confirm': 'Passwords do not match'})
        return attrs

class NotificationsSerializer(serializers.ModelSerializer):
    """
    Serializer for user notifications.
    """
    class Meta:
        model = Notifications
        exclude = ('text',)
