import os
# import stripe

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from carts.models import Cart
from .models import Order
from .utils import generate_order_id


@login_required
def my_orders(request):
	user = request.user
	context = {'orders': user.order_set.all }
	return render(request, 'orders/history.html', context)
