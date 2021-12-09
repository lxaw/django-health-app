from django.contrib import admin

# Register your models here.

from .models import Food

class FoodAdmin(admin.ModelAdmin):
    # what fields display on admin side
    fieldsets = [
        ('Food Name',{'fields':('name',)}),
        ('Kilocals',{'fields':('kcals',)}),
    ]
    # what can be searched
    search_fields = ('name',)
    # filter by characteristics
    list_filter = ('name','author','kcals')

admin.site.register(Food,FoodAdmin)
