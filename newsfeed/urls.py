from django.urls import path
# django login logout views

from . import views as newsfeed_views

app_name = "newsfeed"

urlpatterns = [
    # ex: /newsfeed/index/
    path('index/',newsfeed_views.viewIndex,name="index"),
    # ex: /newfeed/help_request_detail
    path('view/<str:username>/<slug:slug>',newsfeed_views.viewDetail,name="detail"),
    
]