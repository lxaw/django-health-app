from django.urls import path
# django login logout views
from django.contrib.auth import views as auth_views

from . import views as food_views

app_name = "food"

urlpatterns = [
	# ex: /food/
	path('',food_views.viewFoodIndex,name="index"),
	# ex: /food/delete/4/
	path('delete/<int:id>/',food_views.viewFoodDelete,name="food-delete"),
	# ex: /food/prepare/
	path('create-prepare/',food_views.viewFoodPrepare,name="food-create-prepare"),
	# ex: /food/create/
	path('create/',food_views.viewFoodCreate,name="food-create"),
]