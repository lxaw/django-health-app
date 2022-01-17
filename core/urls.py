from django.urls import path

from . import views as core_views

app_name = "core"
urlpatterns = [
	# ex: /
	path('index&np=<int:pg_post>&nhr=<int:pg_help_req>&ndm=<int:pg_dm>/',core_views.viewIndex,name='index'),
	# ex: /about/
	path('',core_views.viewAbout,name='about'),
	# deleting notification
	path('notifications/<str:notification_type>/<int:notification_id>/delete/',core_views.viewNotificationDelete,name="notification-delete"),

	#######################
	# Tips paths
	#######################
	# reading tip
	path('tips/<int:tip_id>/read/',core_views.viewTipRead,name='tip-read'),
	# tip archive
	path('tips/archive&pg_prev_tips=<int:pg_prev_tips>/',core_views.viewTipArchive,name='tip-archive'),

	#######################
	# AJAX paths
	#######################
	path('ajax/index/posts&pg_post=<int:pg_post>&pg_hr=<int:pg_help_req>&pg_dm=<int:pg_dm>/',core_views.aGetNotifPosts,name='ajax-index-posts'),
	path('ajax/index/help_requests&pg_post=<int:pg_post>&pg_hr=<int:pg_help_req>&pg_dm=<int:pg_dm>/',core_views.aGetNotifHelpRequests,name='ajax-index-help-requests'),
	path('ajax/tip/archive/get_tips&pg=<int:pg_prev_tips>/',core_views.aGetTips,name="ajax-tips-archive-prev-tips"),

]