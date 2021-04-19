import json

from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse

from .models import Cart, CartItem
from products.models import Product, ProductImage
from orders.utils import quantity

def my_cart(request):
	user = request.user
	if request.user.is_authenticated:
		cart = Cart.objects.filter(user=user).last()
		if cart == None:
			cart = Cart.objects.create(user=user)
			qty = 0
		else:
			qty = cart.cartitem_set.all().count()
	else:
		qty = 0
		cart = Cart.objects.none()

	if request.method == 'GET':
		context = {'cart': cart,
		'qty': qty,
		}
		return render(request, 'carts/mycart.html', context)

	if request.method == 'POST':
		if request.POST.get('_method') == 'put':
			quantities = [quantity for quantity in request.POST.getlist('quantity')]
			if cart != None:
				for idx, cart_item in enumerate(cart.cartitem_set.all()):
					cart_item.quantity = quantities[idx]
					cart_item.save()

		else:
			print(request.POST)
			product_slug = request.POST.get('product')
			quantity = request.POST.get('quantity')
			product = Product.objects.get(slug=product_slug)
			productimage = product.productimage_set.first()
			variation_color = request.POST.get('color', None)
			variation_size = request.POST.get('size', None)
			if cart != None:
				if product in cart.cartitem_set.all():
					messages.add_message(request, messages.SUCCESS, 'This product has been added to the shopping cart')
				else:
					new_item = CartItem(cart=cart, product=product, 
					productimage=productimage, quantity=quantity)
					new_item.save()
					if variation_color is not None:
						new_item.variation.add(variation_color)
					if variation_size is not None:
						new_item.variation.add(variation_size)
					new_item.save()
					cart.cartitem_set.add(new_item)
					cart = Cart.objects.get(user=user)

		return HttpResponseRedirect(reverse('my_cart'))


def remove_item(request, cart_item_id):
	user = request.user
	cart = Cart.objects.get(user=user)
	cart_item = CartItem.objects.get(id=cart_item_id)
	cart.cartitem_set.remove(cart_item)
	cart.save()
	messages.add_message(request, messages.SUCCESS, 'Product is deleted')
	return HttpResponseRedirect(reverse('my_cart'))