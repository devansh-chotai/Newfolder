from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.clickjacking import xframe_options_exempt

from .forms import (User, UserMailingAddressForm, BalanceUpdateForm,
	UserAccountInfoForm, UserLoginForm)
from .models import UserMailingAddress

# def user_register(request):
# 	form = UserRegistrationForm()

# 	if request.method == 'POST':
# 		form = UserRegistrationForm(request.POST)
# 		if form.is_valid():
# 			username = form.cleaned_data['username']
# 			email = form.cleaned_data['email']
# 			username_exist = User.objects.filter(username=username).last()
# 			email_exist = User.objects.filter(email=email).first()

# 			if username_exist:
# 				messages.add_message(request, messages.ERROR, 'Username already exist. Please choose another one.')

# 			if email_exist:
# 				messages.add_message(request, messages.ERROR, 'The email address has already been registered.')

# 			if form.cleaned_data['password'] == form.cleaned_data['password_confirm']\
# 				and not username_exist and not email_exist:
# 				new_user = User.objects.create(
# 					username=username,
# 					email=email)
# 				new_user.set_password(form.cleaned_data['password'])
# 				new_user.save()

# 				messages.add_message(request, messages.SUCCESS, 'Registered successfully')
# 				return HttpResponseRedirect(reverse('all_products'))
# 			else:
# 				messages.add_message(request, messages.ERROR, "Inconsistent passwords")

# 	context = {'form': form}	
# 	return render(request, 'accounts/register.html', context)
def user_login(request):
	form = UserLoginForm()
	if request.method == 'POST':
		next_url = request.GET.get('next', '')
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				messages.add_message(request, messages.SUCCESS, 'Successfully logged in. Happy shopping!')
				return HttpResponseRedirect(next_url or reverse('all_products'))
			else:
				messages.add_message(request, messages.WARNING, 'Account has not been activated')
		else:
			messages.add_message(request, messages.ERROR, 'Incorrect username or password')
	context = {'form': form}
	return render(request, 'accounts/login.html', context)

@login_required
def user_logout(request):
	logout(request)
	messages.add_message(request, messages.SUCCESS, 'Exit successfully')
	return HttpResponseRedirect(reverse('all_products'))

@login_required
def user_mailing_address(request, do_redirect=None):
	user = request.user
	initial = {}
	if user.usermailingaddress_set.first():
		address = user.usermailingaddress_set.last()
		initial['address1'] = address.address1
		initial['address2'] = address.address2
		initial['city'] = address.city
		initial['state'] = address.state
		initial['zipcode'] = address.zipcode
		initial['phone'] = address.phone

	form = UserMailingAddressForm(initial=initial)
	context = {'form': form, 'do_redirect': do_redirect}

	if request.method == 'POST':
		f = UserMailingAddressForm(request.POST, instance=user)
		if f.is_valid():
			address = user.usermailingaddress_set.create()
			address.address1 = f.cleaned_data['address1']
			address.address2 = f.cleaned_data['address2']
			address.city = f.cleaned_data['city']
			address.state = f.cleaned_data['state']
			address.zipcode = f.cleaned_data['zipcode']
			address.phone = f.cleaned_data['phone']

			address.save()

		messages.add_message(request, messages.SUCCESS, 'Mail address updated successfully')

		if do_redirect == 'yes':
			return HttpResponseRedirect(reverse('user_mailing_address'))
		return HttpResponseRedirect(reverse('user_mailing_address', do_redirect))

	return render(request, 'accounts/mailingaddress.html', context)	

@login_required
def user_account_info(request):
	user = request.user
	form = UserAccountInfoForm(
				initial={
					'username': user.username,
					'email': user.email,
				}
			)
	context = {'form': form}

	if request.method == 'POST':
		f = UserAccountInfoForm(request.POST, instance=user)
		if f.is_valid():
			user.email = f.cleaned_data['email']
			user.username = f.cleaned_data['username']
			user.save()

		messages.add_message(request, messages.SUCCESS, 'Account information updated successfully')

		return HttpResponseRedirect(reverse('user_account_info'))

	return render(request, 'accounts/account.html', context)

@login_required
def user_balance_info(request):
	user = request.user
	form = BalanceUpdateForm(
				initial={
					'balance': user.balance,
				}
			)
	context = {'form': form}

	if request.method == 'POST':
		f = BalanceUpdateForm(request.POST, instance=user)
		if f.is_valid():
			user.balance = f.cleaned_data['balance']
			user.save()

		messages.add_message(request, messages.SUCCESS, 'Money updated successfully')

		return HttpResponseRedirect(reverse('user_balance_info'))

	return render(request, 'accounts/balance.html', context)		