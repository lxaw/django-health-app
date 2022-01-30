#####################################
# HTML routing imports
#####################################
from django.shortcuts import render, reverse, redirect,get_object_or_404,HttpResponseRedirect

# forms
from .forms import UserRegisterForm,CustomUserUpdateForm,CustomUserUpdatePasswordForm

from core.forms import DmForm

# messages on registration / log in
from django.contrib import messages

# json / serializers
from django.http import JsonResponse

# for when need to login to view something
from django.contrib.auth.decorators import login_required

# for forbiddens
from django.http import HttpResponseForbidden

# paginators
from django.core.paginator import Paginator, EmptyPage
from django.template.loader import render_to_string

#################################
# Form imports
#################################
from .forms import SearchUserForm

#################################
# Model imports
#################################

from food.models import Food
from .models import CustomUser
from core.models import NotificationDm

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


# A way to have views with arguments be login views
# kinda cheap
def viewLoginRedirect(request):

	return redirect(reverse("core:index",args=[1,1,1]))

#################################
# Views relating to user profiles
#################################

@login_required
def viewProfile(request,pg_following =1):
	###################################
	# Inputs:
	# request, pg for following users div
	# Outputs:
	# render
	# Utility:
	# view personal profile (only visible to the user themself)
	###################################

	user = request.user


	# followed users
	qsFollowedUsers = user.follows.order_by("username")

	intFollowedUsersPerPage = 1
	# paginate
	paginator_followed_users = Paginator(qsFollowedUsers,intFollowedUsersPerPage)
	try:
		qsFollowedUsers = paginator_followed_users.page(pg_following)
	except:
		qsFollowedUsers = paginator_followed_users.page(paginator_followed_users.num_pages)

	# followers
	# qsFollowerUsers = list(user.followed_by.all())

	context = {
		"dictUserStats" :{
			"strEmail": user.email,
			"strUsername":user.username,
			"strAbout": user.about,
			"boolIsPodPlusMember":user.is_pod_plus_member,
			"intPoints":user.int_points,
			"intDaysActive":user.int_days_active,
			"intUsersHelped":user.int_users_helped,
			"strDateJoined":user.date_joined,
		},
		# followed users
		"qsFollowedUsers":qsFollowedUsers,
	}

	return render(request,'users/profile.html',context = context)

# ajax view to get more followed users
def aGetFollowedUsers(request,pg_following = 1):
	intFollowedUsersPerPage = 1
	qsFollowedUsers = request.user.follows.order_by('username')
	# paginate
	paginator_followed_users = Paginator(qsFollowedUsers,intFollowedUsersPerPage)

	try:
		qsFollowedUsers = paginator_followed_users.page(pg_following)
	except EmptyPage:
		qsFollowedUsers = paginator_followed_users.page(paginator.num_pages)
	
	html_data = render_to_string(
		"users/t/profile_followed_users.html",
		{"qsFollowedUsers":qsFollowedUsers}
	)
	data = {
		"html_data":html_data,
	}

	return JsonResponse(data)

# display form to edit information
@login_required
def viewProfileEditPrepare(request):

	# allow users to edit their information

	context = {
	}

	return render(request,'users/edit.html',context = context)

# process the edited info
@login_required
def viewProfileEdit(request):

	if request.method == 'POST':

		if len(request.FILES) != 0:
			# uploaded a file
			# delete old prof pic, replace with new
			request.user.set_user_profile_picture_default()

		formUpdateForm = CustomUserUpdateForm(request.POST,request.FILES,instance=request.user)
		formUpdatePasswordForm = CustomUserUpdatePasswordForm(data=request.POST,
		instance=request.user)

		if formUpdateForm.is_valid():
			messages.success(request,"Successfully updated profile.")
			# update everything
			if formUpdatePasswordForm.is_valid():
				formUpdateForm.save()
				formUpdatePasswordForm.save()
			# else update without password
			else:
				formUpdateForm.save()
		else:
			print(formUpdateForm.errors)

	return redirect(reverse('users:profile',kwargs={"pg_following":1}))


################################
# Views related to DMs
################################

@login_required
def viewDmIndex(request):
	listmodelDmedUsers = []
	# all the distinct users you have dm'ed

	# format:
	# {"user":lastDm's pubdate}
	dictUserDmDict = {}

	for modelDm in request.user.dm_sender_set.all().order_by('-pub_date'):
		if modelDm.recipient not in dictUserDmDict:
			# add it
			dictUserDmDict[modelDm.recipient] = modelDm.pub_date

	# now loop thru recipient dms, only append to list if 
	# user not in dmDict or if user in but the dm pub date is sooner
	# if dm pub date sooner, just switch out the dm model date
	modelUserSender = None
	for modelDm in request.user.dm_recipient_set.all().order_by('-pub_date'):
		modelUserSender = modelDm.sender
		if modelUserSender not in dictUserDmDict:
			dictUserDmDict[modelDm.sender] = modelDm.pub_date
		else:
			# if the date of the last dm is less than what was recorded, update
			if dictUserDmDict[modelUserSender] < modelDm.pub_date:
				dictUserDmDict[modelUserSender] = modelDm.pub_date
	
	# now sort the dictionary by value
	dictUserDmDict = dict(sorted(dictUserDmDict.items(),key=lambda item: item[1],reverse=True))

	context = {
		"dictUserDmDict":dictUserDmDict,
	}

	return render(request,"users/dm/dm_index.html",context=context)

@login_required
def viewDmPrepareSearch(request):
	formSearchUserForm = SearchUserForm

	
	if "query" in request.GET:
		boolSearched = True
		strSearchStr = request.GET['query']

		# search for user
		listmodelMatchedUsers = []
		for modelUser in CustomUser.objects.filter(username__contains=strSearchStr):
			# can't search for self
			if modelUser != request.user:
				listmodelMatchedUsers.append(modelUser)
				

		context = {
			"formSearchUserForm":formSearchUserForm,
			"boolSearched":boolSearched,
			"strSearchStr":strSearchStr,
			"listmodelMatchedUsers":listmodelMatchedUsers,
		}

		return render(request,'users/dm/dm_prepare-search.html',context=context)
	else:
		# no query yet

		context = {
			"formSearchUserForm":formSearchUserForm,
		}
		return render(request,'users/dm/dm_prepare-search.html',context=context)

@login_required
def viewDmDetail(request,username):
	######################
	# Inputs:
	# request, username of the user to be dm'd by request.user
	######################
	modelUser = get_object_or_404(CustomUser,username=username)

	# get all the messages sent between you and user
	qsSentDms = request.user.dm_sender_set.all().filter(recipient_id=modelUser.id,room=None)
	qsRecievedDms = request.user.dm_recipient_set.all().filter(sender_id=modelUser.id,room=None)

	qsAllDms = qsSentDms.union(qsRecievedDms).order_by('pub_date')

	context = {
		"modelUser":modelUser,
		"qsAllDms":qsAllDms,
	}

	return render(request,'users/dm/dm_detail.html',context=context)


# actually creates the dm
@login_required
def viewDmCreate(request,username):
	######################
	# Inputs:
	# request, str username of the dm'ed user
	######################

	modelOtherUser = get_object_or_404(CustomUser,username=username)

	if request.method == "POST":
		# form for dm
		formDmForm = DmForm(data=request.POST)

		if formDmForm.is_valid():
			# commit = false so can continue editing fields
			modelCreatedDm = formDmForm.save(commit=False)
			# input all other fields besides text
			modelCreatedDm.sender = request.user
			modelCreatedDm.recipient = modelOtherUser
			modelCreatedDm.save()
			messages.success(request,"Direct message sent.")

			# create a notif
			modelNotif = NotificationDm(sender=request.user,recipient = modelOtherUser,
			dm=modelCreatedDm,
			text="{} has sent you a DM in \"General\".".format(request.user.username),
			)
			modelNotif.save()


		else:
			messages.error(request,"Please input text.")
			return redirect(reverse("users:dm-detail",kwargs={"username":username}))
	
	return redirect(reverse("users:dm-detail",kwargs={"username":username}))