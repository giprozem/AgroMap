from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from modeltranslation.admin import TranslationAdmin
from account.models import MyUser, Profile, Notifications
from django.utils.translation import gettext_lazy as _

# This form is used to create a new user.
class UserCreationForm(forms.ModelForm):
    # Password is a required field
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    # Password confirmation is also a required field
    confirm_password = forms.CharField(label=_('Confirm Password'), widget=forms.PasswordInput)

    class Meta:
        # The model used for this form is MyUser.
        model = MyUser
        # Include all fields from the model in the form.
        fields = '__all__'

    def clean_password2(self):
        # Ensure that the password and its confirmation match.
        password = self.cleaned_data.get("password1")
        confirm_password = self.cleaned_data.get("password2")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError(_("Passwords do not match"))
        return confirm_password

    def save(self, commit=True):
        # Save the password in a hashed format.
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["confirm_password"])
        if commit:
            user.save()
        return user

# This form is used to update existing users.
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=_("Password"),
                                         help_text=_("The password can be changed <a href=\"../password/\">here</a>."))

    class Meta:
        model = MyUser
        fields = '__all__'

    def clean_password(self):
        # Ignore any input for the password field and return the initial value instead.
        return self.initial["password"]

# MyUserAdmin is a class that provides administrative options for the MyUser model.
@admin.register(MyUser)
class MyUserAdmin(BaseUserAdmin):
    # When changing a user, use the UserChangeForm.
    form = UserChangeForm
    # When adding a user, use the UserCreationForm.
    add_form = UserCreationForm

    # Define which fields to display in the user list.
    list_display = ('last_login', 'username',)
    list_display_links = ('username',)
    readonly_fields = ("last_login", "date_joined")

    # Define the layout for the change user form.
    fieldsets = ((None, {'fields': ('username', 'password')}),
                 (_('Permissions'), {'fields': ('is_staff', 'is_superuser', 'is_supervisor', 'is_active', 'is_farmer',
                                                'is_employee', 'groups', 'last_login', 'date_joined')}))
    # Define the layout for the add user form.
    add_fieldsets = (
        (None, {'fields': ('username', 'password', 'confirm_password', 'is_staff', 'is_superuser', 'is_supervisor',
                           'is_farmer', 'is_employee', 'groups')}),)

# Register the Profile model with the admin site.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('my_user', 'full_name')
    search_fields = ('full_name', 'my_user__username')

# Register the Notifications model with the admin site.
@admin.register(Notifications)
class NotificationsAdmin(TranslationAdmin):
    list_display = ('user',)
    list_filter = ('user',)
