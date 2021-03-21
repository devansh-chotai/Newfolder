from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model

from .models import UserMailingAddress

User = get_user_model()


class UserMailingAddressForm(ModelForm):
	class Meta:
		model = UserMailingAddress
		labels = {'address1': 'Address Line 1', 'address2': 'Address line 2',
				 'city': 'city', 'state': 'state', 'zipcode': 'Postcode', 'phone': 'phone'}
		fields = ['address1',
				'address2', 'city', 'state', 'zipcode', 'phone']

class UserAccountInfoForm(ModelForm):
	class Meta:
		model = User
		labels = {'email': 'email', 'username': 'username'}
		fields = ['email', 'username']

error_messages={'required': 'must fill'}

class BalanceUpdateForm(ModelForm):	
	class Meta:
		model = User
		labels = {'balance': 'balance'}
		fields = ['balance']


# class UserRegistrationForm(forms.Form):	
# 	username = forms.CharField(error_messages=error_messages, widget=forms.TextInput(attrs={'placeholder': 'username', 'class': 'form-control'}))
# 	email = forms.CharField(error_messages=error_messages, widget=forms.EmailInput(attrs={'placeholder': 'email', 'class': 'form-control'}))
# 	password = forms.CharField(error_messages=error_messages, widget=forms.PasswordInput(attrs={'placeholder': 'password', 'class': 'form-control'}))
# 	password_confirm = forms.CharField(error_messages=error_messages, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password', 'class': 'form-control'}))

class UserLoginForm(forms.Form):	
	username = forms.CharField(error_messages=error_messages, widget=forms.TextInput(attrs={'placeholder': 'username', 'class': 'form-control'}))
	password = forms.CharField(error_messages=error_messages, widget=forms.PasswordInput(attrs={'placeholder': 'password', 'class': 'form-control'}))