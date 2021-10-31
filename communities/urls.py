from django.urls import path

from . import views as communities_views

app_name = "communities"

urlpatterns = [
	# ex: /communities/index/
	path('index',communities_views.viewIndex,name="index"),
]