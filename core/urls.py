from django.urls import path

from . import views as core_views

app_name = "core"
urlpatterns = [
	# ex: /
	path('index/',core_views.viewIndex,name='index'),
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
	path('tips/archive/',core_views.viewTipArchive,name='tip-archive'),
]