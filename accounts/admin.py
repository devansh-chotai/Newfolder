from django.contrib import admin

from .models import UserMailingAddress

class UserMailingAddressAdmin(admin.ModelAdmin):
	search_fields = []
	list_display = ['user', 'address1', 'state']		
	class Meta:
		model = UserMailingAddress

admin.site.register(UserMailingAddress, UserMailingAddressAdmin)
