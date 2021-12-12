#####################################
# HTML routing imports
#####################################
from django.shortcuts import render, redirect,get_object_or_404,HttpResponseRedirect

# forms
from .forms import UserRegisterForm, FoodForm

# messages on registration / log in
from django.contrib import messages

# for when need to login to view something
from django.contrib.auth.decorators import login_required

# for forbiddens
from django.http import HttpResponseForbidden

#################################
# Model imports
#################################

from food.models import Food

#################################
# Package installs
#################################
import numpy as np
from datetime import datetime
import re


def strParsePhoneNumber(strEntry):
	return ''.join(n for n in strEntry if n.isdigit())


#################################
# Views relating to user registration
#################################

def viewRegister(request):
	###################################
	# Inputs:
	# request
	# Outputs:
	# render
	# Utility:
	# View called when registering user
	###################################
	if request.method == "POST":
		# check the phone number
		phone_number = request.POST.get("phone_number")
		pattern = re.compile(r'\d{3}-\d{3}-\d{4}')
		boolValidNumber = bool(pattern.match(phone_number))

		if not boolValidNumber:
			messages.error(request,"Please format number as 3 digits, hyphen, 3 digits, hyphen, 4 digits.")
			return redirect("users:register")

		# if get post request, instantiate form with user data
		form = UserRegisterForm(request.POST)

		if form.is_valid():
			# save the user
			form.save()

			username = form.cleaned_data.get('username')

			messages.success(request, "Account created for {}. You may now log in.".format(username))
			# redirect to this page after creation of account
			return redirect('users:login')

	else:
		form = UserRegisterForm()

	context = {
		'formRegistration':form,
	}

	return render(request,'users/register.html',context=context)

#################################
# Views relating to user profiles
#################################

@login_required
def viewProfile(request):
	###################################
	# Inputs:
	# request
	# Outputs:
	# render
	# Utility:
	# view personal profile (only visible to the user themself)
	###################################

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
	listFoods = []

	if user.uploaded_meals.all():
		arrfloatFood = [i.kcals for i in user.uploaded_meals.all()]

		# Calculating user stats
		floatStd = np.std(arrfloatFood)
		floatMean = np.mean(arrfloatFood)
		floatMedian = np.median(arrfloatFood)
		# for serialization
		listFood = []
		for modelFood in user.uploaded_meals.all():
			dictTemplate = {}
			dictTemplate["date"] = modelFood.date.strftime("%-j")
			dictTemplate["kcals"] = modelFood.kcals
			listFood.append(dictTemplate)

	# followed users
	listFollowedUsers = list(user.follows.all())
	# followers
	listFollowerUsers = list(user.followed_by.all())

	context = {
		"dictUserStats" :{
			"strEmail": user.email,
			"strUsername":user.username,
			"strAbout": user.text_about,
			"boolIsPodPlusMember":user.is_pod_plus_member,
			"intPoints":user.int_points,
			"intDaysActive":user.int_days_active,
			"intUsersHelped":user.int_users_helped,
			"strDateJoined":user.date_joined,
			"intFoodUploadCount":user.uploaded_meals.count(),
			# user stats
			"floatStd":floatStd,
			"floatMean":floatMean,
			"floatMedian":floatMedian,
		},
		"setFood":user.uploaded_meals.all(),
		"listFood":listFood,
		# followed users
		"listFollowerUsers":listFollowerUsers,
		"listFollowedUsers":listFollowedUsers,
	}

	return render(request,'users/profile.html',context = context)

#################################
# Views relating to user Food amounts
#################################

@login_required
def viewUploadFood(request):
	###################################
	# Inputs:
	# request
	# Outputs:
	# render
	# Utility:
	# Upload a food item
	###################################
	# get the user
	user = request.user

	formFoodForm = FoodForm()

	if request.method == "POST":

		formFoodForm = FoodForm(request.POST)

		if formFoodForm.is_valid() and formFoodForm.cleaned_data['kcals'] > 0:
			modelFoodCreated = formFoodForm.save(commit=False)

			modelFoodCreated.author = user
			modelFoodCreated.save()

			return redirect('users:profile')
		else:

			messages.error(request,"Invalid Food amount inputted.")
			return redirect('users:profile')

	context = {
		"formFoodForm":formFoodForm,
	}

	return render(request,'users/upload_food.html',context)

@login_required
def viewDeleteFood(request,id):
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