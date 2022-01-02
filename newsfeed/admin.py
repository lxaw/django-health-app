from django.contrib import admin

from newsfeed.models import HelpRequest,HelpRequestOffer

# Register your models here.

class HelpRequestAdmin(admin.ModelAdmin):
	# Registering the HelpRequest model with admin page

	fieldsets = [
		('Title',{'fields':["title"]}),
		("Author",{"fields":["author"]}),
		('Text Content',{"fields":["text"]}),
		('Tags',{"fields":['tags']}),
		("Date",{"fields":['pub_date']}),
		("Slug",{'fields':['slug']}),
		("Accepted User",{"fields":['accepted_user']}),
		("Accept Date",{"fields":['accept_date']}),
	]

class HelpRequestOfferAdmin(admin.ModelAdmin):
	# Registering the HelpRequestOffer model with admin page

	fieldsets = [
		("Author",{"fields":['author']}),
		("Text Content",{"fields":['text']}),
		("Date",{"fields":["pub_date"]}),
		("Help Request",{"fields":["help_request"]}),
		("Is Accepted?",{"fields":["is_accepted"]}),
	]

admin.site.register(HelpRequest,HelpRequestAdmin)
admin.site.register(HelpRequestOffer,HelpRequestOfferAdmin)