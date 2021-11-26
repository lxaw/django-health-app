from django.urls import path

from . import views as core_views

app_name = "core"
urlpatterns = [
	# ex: /
	path('index/',core_views.viewIndex,name='index'),
	# ex: /about/
	path('',core_views.viewAbout,name='about'),
	# deleting notification
	path('notifications/delete/<int:notification_id>',core_views.viewDeleteNotification,name="notification_delete"),
]