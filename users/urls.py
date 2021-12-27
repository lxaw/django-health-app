from django.urls import path
# django login logout views
from django.contrib.auth import views as auth_views

from . import views as users_views

app_name = "users"

urlpatterns = [
	#####################
	# User basic functions
	# Register, login/out
	#####################
	# ex: /users/register/
	path('register/',users_views.viewRegister,name='register'),
	# ex: /users/login/
	path('login/',auth_views.LoginView.as_view(template_name="users/login.html"),name='login'),
	# ex: /users/logout/
	path('logout/',auth_views.LogoutView.as_view(template_name="users/logout.html"),name='logout'),
	#####################
	# User profile
	#####################
	# ex: /users/profile/
	path('profile/',users_views.viewProfile,name='profile'),
	#####################
	# Food views
	#####################
	# ex: /users/dm/index
	path('dm/index',users_views.viewIndexDMs,name="dm-index"),
	# ex: /users/dm/prepare/
	path('dm/prepare/',users_views.viewDmPrepareSearch,name="dm-prepare"),
	# ex: /users/dm/bob/detail/
	path('dm/<str:username>/detail/',users_views.viewDmDetail,name="dm-detail"),
	# ex: /users/bob/dm/create/
	path('dm/<str:username>/create/',users_views.viewCreateDm,name="dm-create"),
]