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
	path('upload_food',users_views.viewUploadFood,name='upload_food'),
	# ex: /users/delete_kcal/7/
	path('delete_kcal/<int:id>',users_views.viewDeleteFood,name='delete_food'),
	# ex: /users/dm/index
	path('dm/index',users_views.viewIndexDMs,name="dm-index"),
	# ex: /users/dm/prepare/
	path('dm/prepare/',users_views.viewDmPrepareSearch,name="dm-prepare"),
	# ex: /users/dm/prepare/bob/
	path('dm/prepare/<str:username>/',users_views.viewDmPrepareText,name="dm-prepare-text"),
]