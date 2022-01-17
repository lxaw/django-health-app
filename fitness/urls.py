from django.urls import path
# django login logout views
from django.contrib.auth import views as auth_views

from . import views as fitness_views

app_name = "fitness"

urlpatterns = [
	# ex: /fitness/
	path('',fitness_views.viewFitnessIndex,name="index"),
]