from django.contrib import admin

from newsfeed.models import HelpRequest

# Register your models here.

class HelpRequestAdmin(admin.ModelAdmin):

	fieldsets = [
		('Title',{'fields':["title"]}),
		("Author",{"fields":["author"]}),
		('Text Content',{"fields":["text_content"]}),
		('Tags',{"fields":['tags']}),
		("Date",{"fields":['pub_date']}),
		("Slug",{'fields':['slug']}),
	]
admin.site.register(HelpRequest,HelpRequestAdmin)