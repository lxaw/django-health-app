from django.contrib import admin

from .models import TipOfDay,NotificationHelpRequest,NotificationPost

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


admin.site.register(TipOfDay,TipOfDayAdmin)
admin.site.register(NotificationHelpRequest,NotificationHelpRequestAdmin)
admin.site.register(NotificationPost,NotificationPostAdmin)