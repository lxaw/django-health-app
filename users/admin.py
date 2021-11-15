from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea

from .models import CustomUser

from .models import KCalAmount
# Register your models here.


# This all deals with what the admin page shows for custom user class.
class CustomUserAdminConfig(UserAdmin):
	# fields able to search by
	search_fields = ('email','username',)
	# ordering of users
	ordering = ('date_joined',)
	# filtering by characteristics
	list_filter = ('email','username','is_active',
		'is_developer','is_staff','is_pod_plus_member',)
	list_display = ('email','username','is_active',
		'is_developer','is_staff','is_pod_plus_member')
	# fieldsets that display on admin page
	fieldsets = (
		('User Information',{'fields':('email','username',)}),
		('User Permissions',{'fields':('is_staff','is_active','is_developer','is_pod_plus_member')}),
		('User Personal Information',{'fields':('text_about',)}),
		('User Media',{'fields':('profile_picture',)}),
	)

# Register the configuration
admin.site.register(CustomUser,CustomUserAdminConfig)

	

