from django.shortcuts import render
from django.db.models import Q
from accounts.forms import UserLoginForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Product, ProductImage

def all_products(request):
	products = Product.objects.all()
	context = {"products": products}
	return render(request, 'products/all.html', context)

def single_product(request, slug):
	form = UserLoginForm()
	if request.method == 'GET':
		product = Product.objects.get(slug=slug)
		pid = product.productimage_set.all()
		# pi = ProductImage.objects.filter(id=product_id)
		# print(pid)
		context = {"product": product,
					"pid": pid,
					"form": form}
		return render(request, 'products/single.html', context)

	if request.method == 'POST':
		# next_url = request.GET.get('next', '')
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				messages.add_message(request, messages.SUCCESS, 'Successfully logged in. Happy shopping!')
				return HttpResponseRedirect(reverse('all_products'))
			else:
				messages.add_message(request, messages.WARNING, 'Account has not been activated')
		else:
			messages.add_message(request, messages.ERROR, 'Incorrect username or password')
	context = {'form': form}
	return render(request, 'products/single.html', context)


def search_products(request):
	search_term = request.GET.get('term')
	search_results = Product.objects.filter(
					Q(title__icontains=search_term) |
					Q(description__icontains=search_term)
				)
	context = {"products": search_results,
			   "search_term": search_term}
	return render(request, 'products/all.html', context)


