from django.contrib import admin

from .models import Post,HelpRequest

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

class PostAdmin(admin.ModelAdmin):

	fieldsets = [
		("Title",{"fields":['title']}),
		("Author, Text Content",{'fields':['author','text_content']}),
		('Date',{'fields':["pub_date"]}),
		('Slug',{'fields':["slug"]}),
	]

	list_display = ('author','title','text_content')

	list_filter = ['pub_date']

	search_fields = ['author']

admin.site.register(Post,PostAdmin)
admin.site.register(HelpRequest,HelpRequestAdmin)