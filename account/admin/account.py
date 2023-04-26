from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from modeltranslation.admin import TranslationAdmin
from account.models import MyUser, Profile, Notifications


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = '__all__'

    def clean_password2(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password1")
        confirm_password = self.cleaned_data.get("password2")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        return confirm_password

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["confirm_password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = '__all__'

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]



@admin.register(MyUser)
class MyUserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ['id', 'username', 'email']
    fieldsets = ((None, {'fields': ('username', 'password')}),
                 ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_supervisor', 'is_active', 'is_farmer',
                                             'is_employee', 'groups')}))

    add_fieldsets = (
        (None, {'fields': ('username', 'password', 'confirm_password', 'is_staff', 'is_superuser', 'is_supervisor',
                           'is_farmer', 'is_employee', 'groups')}),)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['my_user', 'full_name']


@admin.register(Notifications)
class NotificationsAdmin(TranslationAdmin):
    list_display = ('user', )
    list_filter = ('user', )
