import datetime
import json
from django.shortcuts import render
from django.db.models import Q
from accounts.forms import UserLoginForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.views import View
from django.urls import reverse
from carts.models import Cart
from orders.utils import quantity
from .models import Product, ProductImage, ProductVariation

def all_products(request):
	qty = quantity(request)
	products = Product.objects.all().order_by('?')
	context = {"products": products,
	"qty": qty,}
	return render(request, 'products/all.html', context)


def single_product(request, slug):
	form = UserLoginForm()
	qty = quantity(request)
	dt = datetime.datetime.now()
	shippingdate = (dt + datetime.timedelta(days=3)).strftime("%A, %d %B")
	product = Product.objects.get(slug=slug)
	pid = product.productimage_set.all()

	if request.method == 'POST':
		body = request.body.decode('utf-8')
		data = json.loads(body)
		print(data)
		color_id = data['colorValue']
		size_id = data['sizeValue']
		print(size_id)

		if product.productvariation_set.all().exists():
			if color_id != '':
				title = product.productvariation_set.get(id=color_id)
				pid = title.productimage_set.all()
			else:
				pid = product.productimage_set.all()
			if size_id != '':
				product_price = product.productvariation_set.get(id=size_id).price
				if not product_price:
					product_price = product.price
			else:
				product_price = product.price

		if not pid.exists():
			pid = product.productimage_set.all()
		pid = serializers.serialize('json', pid)
		product_price = str(product_price)

		final_data = {"pid": pid, "price": product_price}

		return JsonResponse({"pid": pid, "price": product_price})
		
	else:
		context = {"product": product,
					"pid": pid,
					"qty": qty,
					"shippingdate":shippingdate,
					}
		return render(request, 'products/single.html', context)

def search_products(request):
	qty = quantity(request)
	search_term = request.GET.get('term')
	filterproducts = request.GET.get('filter2')
	filtersize = request.GET.get('filter3')
	products = Product.objects.all()
	
	if search_term == None:
		search_term = ''

	search_results = Product.objects.filter(
					Q(title__icontains=search_term) |
					Q(description__icontains=search_term)
				).order_by('?')

	if filtersize != None:
		search_results = Product.objects.none()
		if filtersize == 'S':
			for x in products:
				pv = x.productvariation_set.filter(Q(title__icontains='s'))
				if pv:
					search_results = search_results | Product.objects.filter(title=x)
			search_results = search_results.filter(
						Q(title__icontains=search_term) |
						Q(description__icontains=search_term)
			)

		if filtersize == 'M':
			for x in products:
				pv = x.productvariation_set.filter(Q(title__icontains='m'))
				if pv:
					search_results = search_results | Product.objects.filter(title=x)
			search_results = search_results.filter(
						Q(title__icontains=search_term) |
						Q(description__icontains=search_term)
			)	

		if filtersize == 'L':
			for x in products:
				pv = x.productvariation_set.filter( Q(title='l') | Q(title='L'))
				if pv:
					search_results = search_results | Product.objects.filter(title=x)
			search_results = search_results.filter(
						Q(title__icontains=search_term) |
						Q(description__icontains=search_term)
			)

		if filtersize == 'XL':
			for x in products:
				pv = x.productvariation_set.filter( Q(title='xl') | Q(title='XL'))
				if pv:
					search_results = search_results | Product.objects.filter(title=x)
			search_results = search_results.filter(
						Q(title__icontains=search_term) |
						Q(description__icontains=search_term)
			)

		if filtersize == '2XL':
			for x in products:
				pv = x.productvariation_set.filter( Q(title='2xl') | Q(title='2XL'))
				if pv:
					search_results = search_results | Product.objects.filter(Q(title__icontains=x))		


	if filterproducts != None:
		if filterproducts == 'lowtohigh':
			search_results = search_results.order_by('price')
		if filterproducts == 'hightolow':
			search_results = search_results.order_by('-price')
		if filterproducts == 'newest':
			search_results = search_results.order_by('-created')

	recommended_search = search_term[:2]
	recommended_results = Product.objects.filter(
					Q(title__icontains=recommended_search) |
					Q(description__icontains=recommended_search)
				)

	items_found = search_results.count()

	context = {"products": search_results,
			   "search_term": search_term,
			   "qty": qty,
			   "itemsfound": items_found,
			   "recommended_products": recommended_results,
			   "searchterm": search_term,
			   "filtersizevalue": filtersize,
			   }
	return render(request, 'products/all.html', context)


