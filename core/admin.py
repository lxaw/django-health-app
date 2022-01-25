from django.contrib import admin

from .models import (TipOfDay,NotificationHelpRequest,NotificationPost,
NotificationDm,NotificationUser,FeedbackHelpRequest,
FeedbackHelpRequestOffer, RoomDm,Dm)

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

class NotificationDmAdmin(admin.ModelAdmin):
	fieldsets = [
		("Text",{"fields":['text']}),
		("Pub Date",{"fields":['pub_date']}),
		("Sender",{"fields":['sender']}),
		("Recipient",{"fields":['recipient']}),
		("Dm",{"fields":['dm']}),
	]

class NotificationUserAdmin(admin.ModelAdmin):
	fieldsets = [
		("Text",{"fields":['text']}),
		("Pub Date",{"fields":['pub_date']}),
		("Sender",{"fields":['sender']}),
		("Recipient",{"fields":['recipient']}),
		("Linked User",{"fields":['user']}),
	]

###################################
# User feedback
###################################
class FeedbackHelpRequestAdmin(admin.ModelAdmin):
	fieldsets = [
		("Feedback Type",{"fields":['feedback_choice']}),
		("Sender",{"fields":['sender']}),
		("Text (optional)",{"fields":['text']}),
	]
class FeedbackHelpRequestOfferAdmin(admin.ModelAdmin):
	fieldsets = [
		("Feedback Type",{"fields":['feedback_choice']}),
		("Sender",{"fields":['sender']}),
		("Text (optional)",{"fields":['text']}),
	]

###################################
# Rooms
###################################
class RoomDmAdmin(admin.ModelAdmin):
	fieldsets = [
		("Pub date",{"fields":['pub_date']}),
		("Name",{"fields":['name']}),
		("Author",{"fields":['author']}),
		("Partner",{"fields":['partner']}),
	]
###################################
# Dms
###################################
class DmAdmin(admin.ModelAdmin):
	fieldsets = [
		("Pub date",{"fields":['pub_date']}),
		("Recipient",{"fields":['recipient']}),
		("Sender",{"fields":['sender']}),
		("Text",{"fields":['text']}),
		("Room",{"fields":['room']})
	]

# registering the models
admin.site.register(TipOfDay,TipOfDayAdmin)
admin.site.register(NotificationHelpRequest,NotificationHelpRequestAdmin)
admin.site.register(NotificationPost,NotificationPostAdmin)
admin.site.register(NotificationDm,NotificationDmAdmin)
admin.site.register(NotificationUser,NotificationUserAdmin)
admin.site.register(FeedbackHelpRequestOffer,FeedbackHelpRequestOfferAdmin)
admin.site.register(FeedbackHelpRequest,FeedbackHelpRequestAdmin)
admin.site.register(RoomDm,RoomDmAdmin)
admin.site.register(Dm,DmAdmin)