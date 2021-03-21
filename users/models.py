from django.db import models

# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail


class UserManager(BaseUserManager):
    def create_user(
            self, username, email, password,balance=10000,
            commit=True):
        """
        Creates and saves a User with the given email, first name, last name
        and password.
        """
        if not username:
            raise ValueError(_('username is required'))
        if not email:
            raise ValueError(_('email is required'))

        user = self.model(
            username=self.model.normalize_username(username),
            email=self.normalize_email(email),
            balance=10000,
        )

        user.set_password(password)
        if commit:
            user.save(using=self._db)
        return user

    def create_superuser(self, username, email,balance, password=None):
        """
        Creates and saves a superuser with the given email, first name,
        last name and password.
        """
        user = self.create_user(
            username,
            email,
            balance=10000,
            password=password,
            commit=False,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    # password field supplied by AbstractBaseUser
    # last_login field supplied by AbstractBaseUser
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(_('username'),
                                max_length=50,
                                blank=False,
                                unique=True,
                                validators=[username_validator],
                                error_messages={
                                    'invalid': _("Usernames can only use letters, numbers, underscores and periods.."),
                                })

    email = models.EmailField(
        verbose_name=_('email address'), max_length=255, unique=True
    )

    balance = models.DecimalField(decimal_places=2,max_digits=7, blank=False, default=10000)

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )
    # is_superuser field provided by PermissionsMixin
    # groups field provided by PermissionsMixin
    # user_permissions field provided by PermissionsMixin

    date_joined = models.DateTimeField(
        _('date joined'), default=timezone.now
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'balance',]

    # def get_full_name(self):
    #     """
    #     Return the first_name plus the last_name, with a space in between.
    #     """
    #     full_name = '%s' % (self.username )
    #     return full_name.strip()
    #
    # def __str__(self):
    #     return '{} <{}>'.format(self.get_full_name(), self.email)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


# class Signup(models.Model):
#     username = models.CharField(max_length=32, blank=False)
#     name = models.CharField(max_length=32, blank=False)
#     email = models.EmailField(max_length=64, blank=False)
#     password = models.CharField(max_length=64, blank=False)
