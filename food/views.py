from django.shortcuts import render
# messages on registration / log in
from django.contrib import messages

# for when need to login to view something
from django.contrib.auth.decorators import login_required

#####################################
# HTML routing imports
#####################################
from django.shortcuts import render, reverse, redirect,get_object_or_404,HttpResponseRedirect

#####################################
# Necessary models
#####################################
from .models import Food

#################################
# Forms
#################################
from .forms import FoodForm

#################################
# Package installs
#################################
import numpy as np

###################################
# Food views
###################################

@login_required
def viewFoodIndex(request):

	user = request.user

	# performing calculations
	# In reality, we may want the more important / longer calculations to be performed and stored in the model

	# arr of food kcal values
	arrfloatFood = []
	# stddev
	floatStd = 0.0
	# mean
	floatMean = 0.0
	# med
	floatMedian = 0.0
	# list of foodmodels
	listFood = []

	if user.uploaded_meals.all():
		arrfloatFood = [i.kcals for i in user.uploaded_meals.order_by('-pub_date')]

		# Calculating user stats
		floatStd = np.std(arrfloatFood)
		floatMean = np.mean(arrfloatFood)
		floatMedian = np.median(arrfloatFood)
		# for serialization
		for modelFood in user.uploaded_meals.all():
			dictTemplate = {}
			dictTemplate["pub_date"] = modelFood.pub_date.strftime("%-j")
			dictTemplate["kcals"] = modelFood.kcals
			listFood.append(dictTemplate)


	context = {
		"dictUserStats" :{
			"intFoodUploadCount":user.uploaded_meals.count(),
			# user stats
			"floatStd":floatStd,
			"floatMean":floatMean,
			"floatMedian":floatMedian,
		},
		"setFood":user.uploaded_meals.all(),
		"listFood":listFood,
	}

	return render(request,'food/index.html',context)

@login_required
def viewFoodPrepare(request):
	###################################
	# Inputs:
	# request
	# Outputs:
	# render
	# Utility:
	# Upload a food item
	###################################

	context = {

	}

	return render(request,'food/food_prepare.html',context)

@login_required
def viewFoodCreate(request):
	# creates a food object
	formFoodForm = FoodForm()

	if request.method == "POST":
		formFoodForm = FoodForm(request.POST)

		if formFoodForm.is_valid():
			if not formFoodForm.cleaned_data['kcals'] > 0:
				messages.warning(request,"Kilocalories must be positive.")
				return redirect('food:index')
			else:
				modelFood = formFoodForm.save(commit=False)
				modelFood.author = request.user
				modelFood.save()
				return redirect('food:index')

	messages.warning(request,"Incorrect form data. Please try again.")	
	return redirect('food:food-create-prepare')

@login_required
def viewFoodDelete(request,id):
	###################################
	# Inputs:
	# request, int id
	# Outputs:
	# HttpResponse
	# Utility:
	# Delete a food item
	###################################
	modelFoodInstance = get_object_or_404(Food,id=id)

	# check if the current user is author, if not dont do anything
	if request.user != modelFoodInstance.author:
		return HttpResponseRedirect('/')

	# delete the Food amount
	# NOTE:
	# be sure to check that this will not affect
	# any user attributes in the future.
	modelFoodInstance.delete()

	return HttpResponseRedirect('/')