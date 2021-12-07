from django.urls import path
# django login logout views

from . import views as newsfeed_views

app_name = "newsfeed"

urlpatterns = [
    # ex: /newsfeed/index/
    path('index',newsfeed_views.viewIndex,name="index"),
	##################
	# URLS for Ask for Help
	##################
    # ex: /newfeed/help-request/lex/my-title
    path('view-request/<str:username>/<slug:slug>',newsfeed_views.viewDetail,name="detail"),
    # ex: /newsfeed/help-request/tag/my-tag 
    path('by-tag/tag/<str:tag>',newsfeed_views.viewDetailByTag,name="detail_tag"),
	# ex: /newsfeed/request_help
	path('request_help',newsfeed_views.viewRequestHelp,name="request_help"),
	# creating a request for help
	path('request_help/create',newsfeed_views.viewCreateHelpRequest,name="create_help_request"),
	# delete help request
	path('request_help/delete/<int:id>',newsfeed_views.viewDeleteHelpRequest,name="delete_help_request"),
]