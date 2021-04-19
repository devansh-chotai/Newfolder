import random
import string
from carts.models import Cart

def generate_order_id():
	chars = string.ascii_uppercase + string.digits
	order_number = "".join(random.choice(chars) for _ in range(8))
	return order_number

def quantity(request):
	user = request.user
	if request.user.is_authenticated == False:
		qty = 0
	else:
		cart = Cart.objects.filter(user=user).last()
		if cart == None:
			qty = 0
		else:
			qty = cart.cartitem_set.all().count()
	return qty
