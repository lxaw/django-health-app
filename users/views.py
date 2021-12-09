#################################
# Django models
#################################
from django.shortcuts import render, redirect,get_object_or_404

# forms
from .forms import UserRegisterForm, KCalAmountForm

# messages on registration / log in
from django.contrib import messages

# for when need to login to view something
from django.contrib.auth.decorators import login_required

# for forbiddens
from django.http import HttpResponseForbidden

#################################
# SocialPOD Models
#################################

from .models import KCalAmount

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

	user = request.user


	# performing calculations
	# In reality, we may want the more important / longer calculations to be performed and stored in the model
	# Standard deviation

	arrfloatKCals = [i.amount for i in user.kcalamount_set.all()]

	# Calculating user stats
	floatStd = np.std(arrfloatKCals)
	floatMean = np.mean(arrfloatKCals)
	floatMedian = np.median(arrfloatKCals)

	# for serialization
	listKCals = []
	for modelKCal in user.kcalamount_set.all():
		dictTemplate = {}
		dictTemplate["date"] = modelKCal.date.strftime("%-j")
		dictTemplate["amount"] = modelKCal.amount
		listKCals.append(dictTemplate)
	

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
			"intKCalUploadCount":user.kcalamount_set.count(),
			# user stats
			"floatStd":floatStd,
			"floatMean":floatMean,
			"floatMedian":floatMedian,
		},
		"setKCals":user.kcalamount_set.all(),
		"listKCals":listKCals,
		# followed users
		"listFollowerUsers":listFollowerUsers,
		"listFollowedUsers":listFollowedUsers,
	}

	return render(request,'users/profile.html',context = context)

#################################
# Views relating to user KCal amounts
#################################

@login_required
def viewUploadKCals(request):
	# get the user
	user = request.user

	modelKCalInstance = KCalAmount()
	formKCalForm = KCalAmountForm(instance = modelKCalInstance)

	if request.method == "POST":

		formKCalForm = KCalAmountForm(request.POST)

		if formKCalForm.is_valid() and formKCalForm.cleaned_data['amount'] > 0:
			print('here')
			modelKCalCreated = formKCalForm.save(commit=False)

			modelKCalCreated.author = user
			modelKCalCreated.save()

			return redirect('users:profile')
		else:

			messages.error(request,"Invalid KCal amount inputted.")
			return redirect('users:profile')

	context = {
		"formKCalForm":formKCalForm,
	}

	return render(request,'users/upload_kcals.html',context)

@login_required
def viewDeleteKCal(request,pk):
	modelKCalInstance = get_object_or_404(KCalAmount,pk=pk)

	user = request.user
	if modelKCalInstance.author != user:
		return HttpResponseForbidden("Not your kcals!")

	context = {
		'modelKCalInstance':modelKCalInstance,
	}

	if request.method == "POST":
		# delete the KCal amount
		# NOTE:
		# be sure to check that this will not affect
		# any user attributes in the future.
		modelKCalInstance.delete()

		messages.success(request,"KCal value successfully deleted.")

		# redirect to profile
		return redirect("users:profile")

	return render(request,'users/delete_kcal.html',context)
