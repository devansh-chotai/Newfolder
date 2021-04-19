from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic.edit import FormView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters


from .forms import (User, UserMailingAddressForm, BalanceUpdateForm,
	UserAccountInfoForm, UserLoginForm)
from .models import UserMailingAddress
from carts.models import Cart
from orders.utils import quantity

@xframe_options_exempt
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
	qty = quantity(request)
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
	context = {'form': form, 'do_redirect': do_redirect, 'qty': qty}

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

		messages.add_message(request, messages.SUCCESS, 'Shipping address updated successfully')

		if do_redirect == 'yes':
			return HttpResponseRedirect(reverse('user_mailing_address'))
		return HttpResponseRedirect(reverse('user_mailing_address', do_redirect))

	return render(request, 'accounts/mailingaddress.html', context)	

@login_required
def user_account_info(request):
	user = request.user
	qty = quantity(request)
	form = UserAccountInfoForm(
				initial={
					'username': user.username,
					'email': user.email,
				}
			)
	context = {'form': form, 'qty': qty}

	if request.method == 'POST':
		f = UserAccountInfoForm(request.POST, instance=user)
		if f.is_valid():
			user.email = f.cleaned_data['email']
			user.username = f.cleaned_data['username']
			user.save()

			messages.add_message(request, messages.SUCCESS, 'Account information updated successfully')

			return HttpResponseRedirect(reverse('user_account_info'))
		else:
			messages.add_message(request, messages.ERROR, 'Usename/E-mail already exists.')
			return HttpResponseRedirect(reverse('user_account_info'))


	return render(request, 'accounts/account.html', context)

@login_required
def user_balance_info(request):
	user = request.user
	qty = quantity(request)
	form = BalanceUpdateForm(
				initial={
					'balance': user.balance,
				}
			)
	context = {'form': form, 'qty':qty}

	if request.method == 'POST':
		f = BalanceUpdateForm(request.POST, instance=user)
		if f.is_valid():
			user.balance = f.cleaned_data['balance']
			user.save()

		messages.add_message(request, messages.SUCCESS, 'Money updated successfully')

		return HttpResponseRedirect(reverse('user_balance_info'))

	return render(request, 'accounts/balance.html', context)	

class PasswordContextMixin:
    extra_context = None
    def get_context_data(self, **kwargs):
        user = self.request.user
        if self.request.user.is_authenticated == False:
            qty = 0
        else:
            cart = Cart.objects.filter(user=user).last()
            if cart == None:
                qty = 0
            else:
                qty = cart.cartitem_set.all().count()
        extra_context = {'qty': qty}
        # print(extra_context)
        context = super().get_context_data(**kwargs)
        context.update({
            **(extra_context or {})
        })
        print(context)
        return context

class PasswordChangeView(PasswordContextMixin, FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('change_password')
    template_name = 'resetpassword.html'

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.SUCCESS, 'Password changed successfully')
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)