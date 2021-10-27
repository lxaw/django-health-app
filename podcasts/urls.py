from django.urls import path

from . import views as podcasts_views

app_name = "podcasts"

urlpatterns = [
	# ex: /podcasts/index/
	path('index',podcasts_views.viewIndex,name="index"),
]