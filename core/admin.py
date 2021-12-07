from django.contrib import admin

from .models import TipOfDay,Notification

# Register your models here.

class TipOfDayAdmin(admin.ModelAdmin):
	fieldsets = [
		("Text Content",{"fields":['text_content']}),
		("Tags",{"fields":['tags']}),
		("Urls",{"fields":['url']}),
	]
	search_fields = ['tag','text_content']

class NotificationAdmin(admin.ModelAdmin):
	fieldsets = [
		("sender",{"fields":['sender']}),
		("recipient",{"fields":['recipient']}),
		("message",{"fields":['message']}),
		("pub_date",{"fields":['pub_date']}),
		("read",{"fields":['read']}),
	]

admin.site.register(TipOfDay,TipOfDayAdmin)
admin.site.register(Notification, NotificationAdmin)
