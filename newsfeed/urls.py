from django.urls import path
# django login logout views

from . import views as newsfeed_views

app_name = "newsfeed"

urlpatterns = [
    # ex: /newsfeed/index/
    path('index/',newsfeed_views.viewIndex,name="index"),
    # ex: /newfeed/help-request/lex/my-title
    path('view-request/<str:username>/<slug:slug>',newsfeed_views.viewDetail,name="detail"),
    # ex: /newsfeed/help-request/tag/my-tag 
    path('by-tag/tag/<str:tag>',newsfeed_views.viewDetailByTag,name="detail_tag"),
]