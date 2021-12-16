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
    path('view-request/<str:username>/<slug:slug>/',newsfeed_views.viewDetailHelpRequest,name="help-request-detail"),
    # ex: /newsfeed/help-request/tag/my-tag 
    path('by-tag/tag/<str:tag>/',newsfeed_views.viewIndexByTag,name="help-request-index-tag"),
	# ex: /newsfeed/request_help
	path('request-help/',newsfeed_views.viewRequestHelp,name="help-request-prepare"),
	# creating a request for help
	path('request-help/create/',newsfeed_views.viewCreateHelpRequest,name="help-request-create"),
	# delete help request
	path('request-help/delete/<int:id>/',newsfeed_views.viewDeleteHelpRequest,name="help-request-delete"),
	##################
	# URLS for Help Request Offers
	##################
	# creating a help request offer
	path('request-help/<str:username>/<slug:slug>/offer/create/',newsfeed_views.viewCreateHelpRequestOffer,name="help-request-offer-create"),
	# viewing a help request offer
	path('request-help/<str:username>/<slug:slug>/offer/<int:id>/detail/',newsfeed_views.viewDetailHelpRequestOffer,name="help-request-offer-detail"),
	# accept a help request offer
	path('request-help/<str:username>/<slug:slug>/offer/<int:id>/accept/',newsfeed_views.viewAcceptHelpRequestOffer,name="help-request-offer-accept"),
	# reject help request offer
	path('request-help/<str:username>/<slug:slug>/offer/<int:id>/reject/',newsfeed_views.viewRejectHelpRequestOffer,name="help-request-offer-reject"),
	##################
	# URLS for old Help Requests
	##################
	path('archives/',newsfeed_views.viewDetailArchive,name="help-request-archive-detail"),
]