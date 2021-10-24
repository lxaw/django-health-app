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
	# ex: /users/upload_kcals/
	path('upload_kcals',users_views.viewUploadKCals,name='upload_kcals'),
	# ex: /users/delete_kcal/7/
	path('delete_kcal/<int:pk>',users_views.viewDeleteKCal,name='delete_kcal'),
]