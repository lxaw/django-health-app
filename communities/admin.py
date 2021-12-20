from django.contrib import admin

from .models import Post, Comment

# Register your models here.

############################
# Posts
############################

class CommentInline(admin.TabularInline):
	fieldsets = [
		("Post",{"fields":['post']}),
		("Author",{"fields":['author']}),
		("Body",{"fields":['body']}),
		("Parent",{"fields":['parent']}),
	]
	model = Comment

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

	inlines = [CommentInline]


admin.site.register(Post,PostAdmin)