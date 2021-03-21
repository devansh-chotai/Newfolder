from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

from carts.models import Cart
from .models import Order
from .utils import generate_order_id
from carts.models import Cart, CartItem
from .models import Order
from .utils import generate_order_id

User = get_user_model()


@login_required
def my_orders(request):
	user = request.user
	context = {'orders': user.order_set.all }
	return render(request, 'orders/history.html', context)


@login_required
def new_orders(request):
	if request.session.get('cart_id'):
		cart_id = request.session.get('cart_id')
		cart = Cart.objects.get(id=cart_id)
	else:
		cart = Cart.objects.create()
		request.session['cart_id'] = cart.id
	user = request.user
	mailing_address = user.usermailingaddress_set.last()
	cart_id = request.session.get('cart_id')
	cart = Cart.objects.get(id=cart_id)
	order_total = str(cart.get_total())
	context = {'mailing_address': mailing_address,
			   'order_total': order_total,
			   'cart' : cart,
			   }
	if request.method == 'POST':
		if mailing_address is None or mailing_address.address1 == '':
			messages.add_message(request, messages.ERROR, 'Please provide your Shipping address')
			return HttpResponseRedirect(reverse('new_orders'))		

		order = Order(
			user=user,
			cart=cart,
			mailing_address=mailing_address,
 			order_id=generate_order_id(),
			subtotal=cart.get_subtotal(),
			tax=cart.get_tax(),
			total=cart.get_total()
			)		

		order.save()
		BalanceUpdate = User.objects.filter(username=user).first()
		BalanceUpdate.balance = user.balance - cart.get_total()
		BalanceUpdate.save()
		
		del request.session['cart_id']
		del request.session['total_items']

		messages.add_message(request, messages.SUCCESS, 'Order submitted successfully.')
		return HttpResponseRedirect(reverse('my_orders'))
	return render(request, 'orders/new.html', context)