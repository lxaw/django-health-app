from django.contrib import admin

from .models import TipOfDay

# Register your models here.

class TipOfDayAdmin(admin.ModelAdmin):
	fieldsets = [
		("Text Content",{"fields":['text_content']}),
		("Tags",{"fields":['tags']})
	]
	search_fields = ['tag','text_content']

admin.site.register(TipOfDay,TipOfDayAdmin)
