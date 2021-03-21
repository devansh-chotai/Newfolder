from django.contrib import admin

# Register your models here.
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User


class AddUserForm(forms.ModelForm):
    """
    New User Form. Requires password confirmation.
    """
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput
    )
    # password2 = forms.CharField(
    #     label='Confirm password', widget=forms.PasswordInput
    # )

    class Meta:
        model = User
        fields = ('username', 'email', 'balance')

    def clean_passwordt(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        # password2 = self.cleaned_data.get("password2")
        # if password and password and password != password:
        #     raise forms.ValidationError("Passwords do not match")
        return password

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UpdateUserForm(forms.ModelForm):
    """
    Update User Form. Doesn't allow changing password in the Admin.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            'username', 'password', 'email','balance', 'is_active',
            'is_staff'
        )

    def clean_password(self):
# Password can't be changed in the admin
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UpdateUserForm
    add_form = AddUserForm

    list_display = ('username', 'email', 'balance', 'is_staff')
    list_filter = ('is_staff', )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ['email', 'balance']}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'username', 'email', 'password', 'balance'
                    # 'password2'
                )
            }
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username', 'email', 'balance')
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
