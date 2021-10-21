from django.urls import path

from . import views as users_views

app_name = "users"

urlpatterns = [
	# ex: /users/register/
	path('register/',users_views.viewRegister,name='register'),
]