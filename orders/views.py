from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

from carts.models import Cart
from products.models import Product
from .models import Order
from .utils import generate_order_id
from carts.models import Cart, CartItem
from .models import Order
from .utils import generate_order_id, quantity

User = get_user_model()


@login_required
def my_orders(request):
	user = request.user
	qty = quantity(request)
	context = {'orders': user.order_set.all().order_by('-id'),
	'qty':qty,}
	return render(request, 'orders/history.html', context)


@login_required
def new_orders(request):
	user = request.user
	cart = Cart.objects.filter(user=user).last()
	qty = quantity(request)
		
	if cart.cartitem_set.first() == None:
		return redirect('my_cart')
	user = request.user
	mailing_address = user.usermailingaddress_set.last()
	order_total = str(cart.get_total())
	context = {'mailing_address': mailing_address,
			   'order_total': order_total,
			   'cart' : cart,
			   'qty': qty,
			   }
	if request.method == 'POST':
		if mailing_address is None or mailing_address.address1 == None or mailing_address.address2 == None:
			messages.add_message(request, messages.ERROR, 'Please provide your <a href="/account/mailing/">Shipping address</a>', extra_tags='safe')
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

		BalanceUpdate = User.objects.get(username=user)
		BalanceUpdate.balance = user.balance - cart.get_total()
		BalanceUpdate.save()
		
		Cart.objects.filter(user=user).update(user='')

		messages.add_message(request, messages.SUCCESS, 'Order submitted successfully.')
		return HttpResponseRedirect(reverse('my_orders'))
	return render(request, 'orders/new.html', context)