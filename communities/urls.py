from django.urls import path

from . import views as communities_views

app_name = "communities"

urlpatterns = [
	# ex: /communities/index/
	path('index',communities_views.viewIndex,name="index"),
	# ex: /communities/create_post/
	path('create_post',communities_views.viewCreatePost,name="create_post"),
	# ex: /communities/posts/username/slug-my-post-title/create_comment/
	path('posts/<str:username>/<slug:slug>/create_comment',communities_views.viewCreateComment,name="create_comment" ),
	# ex: /communities/posts/username/slug-my-post-title/delete_comment/
	path('posts/delete_comment/<int:comment_id>',communities_views.viewDeleteComment,name="delete_comment" ),
	# ex: /communities/posts/username/slug-my-post-title/
	path('posts/<str:username>/<slug:slug>',communities_views.viewPostDetail,name="post_detail"),
	# ex: /communities/like/2/
	path('like_post/<int:post_id>',communities_views.viewLikePost,name="like_post"),
	# ex: /communities/profile/username/
	path('profile/<str:username>',communities_views.viewProfile,name="profile"),
]