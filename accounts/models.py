from django.db import models
from django.conf import settings
from localflavor.in_.in_states import STATE_CHOICES



class UserMailingAddress(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	address1 = models.CharField(max_length=200, null=True, blank=True)
	address2 = models.CharField(max_length=200, null=True, blank=True)
	city = models.CharField(max_length=50, null=True, blank=True)
	state = models.CharField(max_length=50, choices=STATE_CHOICES, blank=True)
	zipcode = models.CharField(max_length=20, null=True, blank=True)
	phone = models.CharField(max_length=20, null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return "<UserMailingAddress: %d - %s>" % (self.user.id, self.user.username)

	def is_complete(self):
		if not self.first_name or not self.last_name or not self.address1 or not self.city\
			or not self.state or not self.zipcode or not self.phone:
			return False
		return True

