from django.contrib import admin

from .models import TipOfDay,NotificationHelpRequest,NotificationPost, NotificationDirectMessage,NotificationUser

# Register your models here.

class TipOfDayAdmin(admin.ModelAdmin):
	fieldsets = [
		("Text Content",{"fields":['text']}),
		("Tags",{"fields":['tags']}),
		("Urls",{"fields":['url']}),
	]
	search_fields = ['tag','text']

class NotificationHelpRequestAdmin(admin.ModelAdmin):
	fieldsets = [
		("Text",{"fields":['text']}),
		("Pub Date",{"fields":['pub_date']}),
		("Sender",{"fields":['sender']}),
		("Recipient",{"fields":['recipient']}),
		("Help Request",{"fields":['Help Request']}),
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