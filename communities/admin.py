from django.contrib import admin

from .models import Post

# Register your models here.

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