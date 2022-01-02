from django.urls import path

from . import views as communities_views

app_name = "communities"

# ###############################
# NOTE: Order matters!
# ###############################

urlpatterns = [
	# ex: /communities/index/
	path('index/<int:page>/',communities_views.viewIndex,name="index"),

	##################
	# URLS for Posts
	##################
	# CREATING A POST
	path('posts/post-create/',communities_views.viewPostCreate,name="post-create"),
	# DELETING A POST
	path('posts/post-delete/<int:post_id>',communities_views.viewPostDelete,name="post-delete"),
	# VIEWING A POST
	path('posts/view/<str:username>/<slug:slug>/',communities_views.viewPostDetail,name="post-detail"),
	# prepare a post
	path('posts/prepare/',communities_views.viewPostPrepare,name="post-prepare"),

	##################
	# URLS for Posts Actions (Like)
	##################
	path('post-like/<int:post_id>/',communities_views.viewLikeUnlikePost,name="post-like-unlike"),

	##################
	# URLS for Posts Comments
	##################
	# ex: /communities/posts/username/slug-my-post-title/create_comment/
	path('posts/<str:username>/<slug:slug>/comment-create/',communities_views.viewCreateComment,name="comment-create"),
	# ex: /communities/posts/username/slug-my-post-title/delete_comment/
	path('posts/comment-delete/<int:comment_id>/',communities_views.viewDeleteComment,name="comment-delete"),

	##################
	# URLS for Public Profiles
	##################
	# ex: /communities/profile/username/
	path('profile/<str:username>/',communities_views.viewProfile,name="profile"),
	##################
	# URLS for Following
	##################
	path('following/add_remove_follow/<str:username>/',communities_views.viewAddRemoveFollow,name="follow-add-remove"),

	##################
	# URLS for Leaderboard
	##################
	path("leaderboard/index/",communities_views.viewLeaderboardIndex,name='leaderboard-index'),
]