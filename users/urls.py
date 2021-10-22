from django.urls import path
# django login logout views
from django.contrib.auth import views as auth_views

from . import views as users_views

app_name = "users"

urlpatterns = [
	# ex: /users/register/
	path('register/',users_views.viewRegister,name='register'),
	# ex: /users/login/
	path('login/',auth_views.LoginView.as_view(template_name="users/login.html"),name='login'),
	# ex: /users/logout/
	path('logout/',auth_views.LogoutView.as_view(template_name="users/logout.html"),name='logout'),
	# ex: /users/profile/
	path('profile/',users_views.viewProfile,name='profile'),
]