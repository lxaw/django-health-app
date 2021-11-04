from django.urls import path

from . import views as communities_views

app_name = "communities"

urlpatterns = [
	# ex: /communities/index/
	path('index',communities_views.viewIndex,name="index"),
	# ex: /communities/create_post/
	path('create_post',communities_views.viewCreatePost,name="create_post"),
	# ex: /communities/like/2/
	path('communities/like_post/<int:post_id>',communities_views.viewLikePost,name="like_post")
]