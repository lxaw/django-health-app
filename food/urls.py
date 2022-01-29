from django.urls import path
# django login logout views
from django.contrib.auth import views as auth_views

from . import views as food_views

app_name = "food"

urlpatterns = [
	# ex: /food/
	path('',food_views.viewFoodIndex,name="index"),
	# detail a food entry
	path("entry/<int:id>/detail/",food_views.viewFoodEntryDetail,name='food-entry-detail'),
	# ex: /food/delete/4/
	path('entry/<int:id>/delete/',food_views.viewFoodDelete,name="food-entry-delete"),
	# ex: /food/prepare/
	path('prepare/',food_views.viewFoodPrepare,name="food-entry-prepare"),
	# ex: /food/create/
	path('create/',food_views.viewFoodCreate,name="food-entry-create"),

]