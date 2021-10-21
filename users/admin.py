from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea

from .models import CustomUser
# Register your models here.

# This all deals with what the admin page shows for custom user class.
class CustomUserAdminConfig(UserAdmin):
	# fields able to search by
	search_fields = ('email','user_name',)
	# ordering of users
	ordering = ('date_joined',)
	# filtering by characteristics
	list_filter = ('email','user_name','is_active',
		'is_developer','is_staff','is_pod_plus_member',)
	list_display = ('email','user_name','is_active',
		'is_developer','is_staff','is_pod_plus_member')
	# fieldsets that display on admin page
	fieldsets = (
		('User Information',{'fields':('email','user_name',)}),
		('User Permissions',{'fields':('is_staff','is_active','is_developer','is_pod_plus_member')}),
		('User Personal Information',{'fields':('text_about',)})
	)

# Register the configuration
admin.site.register(CustomUser,CustomUserAdminConfig)

	

