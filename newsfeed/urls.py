from django.urls import path
# django login logout views

from . import views as newsfeed_views

app_name = "newsfeed"

urlpatterns = [
    # ex: /newsfeed/index/
    path('index&page=<int:page>/',newsfeed_views.viewIndex,name="index"),
	##################
	# URLS for Ask for Help
	##################
    # ex: /newfeed/help-request/lex/my-title
    path('request-help/<str:username>/<slug:slug>/',newsfeed_views.viewHelpRequestDetail,name="help-request-detail"),
    # ex: /newsfeed/request-help/tag/my-tag 
    path('request-help/by-tag/tag/<str:tag>/',newsfeed_views.viewHelpRequestOfferDetailTag,name="help-request-index-tag"),
	# ex: /newsfeed/request_help
	path('request-help/',newsfeed_views.viewHelpRequestPrepare,name="help-request-prepare"),
	# creating a request for help
	path('request-help/create/',newsfeed_views.viewHelpRequestCreate,name="help-request-create"),
	# delete help request
	path('request-help/<str:username>/<slug:slug>/delete/',newsfeed_views.viewHelpRequestDelete,name="help-request-delete"),

	# prepare to reset user
	path('request-help/<str:username>/<slug:slug>/reset-prepare/',newsfeed_views.viewHelpRequestAcceptedUserResetPrepare,name="help-request-accepted-user-reset-prepare"),
	# actually reset user
	path('request-help/<str:username>/<slug:slug>/reset/',newsfeed_views.viewHelpRequestAcceptedUserReset,name="help-request-accepted-user-reset"),

	##################
	# URLS for Help Request Offers
	##################
	# creating a help request offer
	path('request-help/<str:username>/<slug:slug>/offer/create/',newsfeed_views.viewHelpRequestOfferCreate,name="help-request-offer-create"),
	# viewing a help request offer
	path('request-help/<str:username>/<slug:slug>/offer/<int:id>/detail/',newsfeed_views.viewHelpRequestOfferDetail,name="help-request-offer-detail"),
	# accept a help request offer
	path('request-help/<str:username>/<slug:slug>/offer/<int:id>/accept/',newsfeed_views.viewHelpRequestOfferAccept,name="help-request-offer-accept"),
	# reject help request offer
	path('request-help/<str:username>/<slug:slug>/offer/<int:id>/reject/',newsfeed_views.viewHelpRequestOfferReject,name="help-request-offer-reject"),
	# remove accepted offer prepare
	# note that both the creator of the help request offer AND the creator of the help request can remove offers
	# remove accepted offer
	path('request-help/<str:username>/<slug:slug>/offer/<int:id>/delete/',newsfeed_views.viewHelpRequestOfferDelete,name='help-request-offer-delete'),

	##################
	# URLs for dms
	##################
	# detail a conversation
	path('dm/<str:hr_author_username>&<str:hr_accepted_user_username>/<str:room_name>/',newsfeed_views.viewDmDetail,name='help-request-dm-detail'),
	# create a dm
	path('dm/<str:hr_author_username>&<str:hr_accepted_user_username>/<str:room_name>/create/',newsfeed_views.viewDmCreate,name='help-request-dm-create'),

	##################
	# URLS for old Help Requests
	##################
	path('archive/',newsfeed_views.viewHelpRequestArchiveDetail,name="help-request-archive-detail"),
]