from django.contrib import admin

from .models import TipOfDay,NotificationHelpRequest,NotificationPost, NotificationDirectMessage,NotificationUser

# Register your models here.

class TipOfDayAdmin(admin.ModelAdmin):
	fieldsets = [
		("Text Content",{"fields":['text']}),
		("Tags",{"fields":['tags']}),
		("Responded Users",{"fields":['responded_users']}),
		("Day Number",{"fields":["day_number"]}),
	]

	# what to display as a row on admin page
	list_display = ['day_number','tags']
	
	# what can be filtered
	list_filter = ('tags',)

	# what can be searched
	search_fields = ['day_number','tags','text']

	# ordering
	ordering = ('day_number',)

###################################
# Notifications
###################################

class NotificationHelpRequestAdmin(admin.ModelAdmin):
	fieldsets = [
		("Text",{"fields":['text']}),
		("Pub Date",{"fields":['pub_date']}),
		("Sender",{"fields":['sender']}),
		("Recipient",{"fields":['recipient']}),
		("Help Request",{"fields":['help_request']}),
	]


class NotificationPostAdmin(admin.ModelAdmin):
	fieldsets = [
		("Text",{"fields":['text']}),
		("Pub Date",{"fields":['pub_date']}),
		("Sender",{"fields":['sender']}),
		("Recipient",{"fields":['recipient']}),
		("Post",{"fields":['post']}),
	]

class NotificationDirectMessageAdmin(admin.ModelAdmin):
	fieldsets = [
		("Text",{"fields":['text']}),
		("Pub Date",{"fields":['pub_date']}),
		("Sender",{"fields":['sender']}),
		("Recipient",{"fields":['recipient']}),
		("Direct Message",{"fields":['direct_message']}),
	]

class NotificationUserAdmin(admin.ModelAdmin):
	fieldsets = [
		("Text",{"fields":['text']}),
		("Pub Date",{"fields":['pub_date']}),
		("Sender",{"fields":['sender']}),
		("Recipient",{"fields":['recipient']}),
		("Linked User",{"fields":['user']}),
	]

admin.site.register(TipOfDay,TipOfDayAdmin)
admin.site.register(NotificationHelpRequest,NotificationHelpRequestAdmin)
admin.site.register(NotificationPost,NotificationPostAdmin)
admin.site.register(NotificationDirectMessage,NotificationDirectMessageAdmin)
admin.site.register(NotificationUser,NotificationUserAdmin)