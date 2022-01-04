###########################
# Django functions
###########################
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

###########################
# Necessary models
###########################
from .models import TipOfDay,NotificationPost,NotificationHelpRequest,NotificationUser
from users.models import CustomUser

###########################
# Necessary imports
###########################
from datetime import date
from datetime import datetime
import random

from core.base_functions import boolModelOwnershipCheck

# Create your views here.

def viewAbout(request):
	###################################
	# Inputs:
	# request
	# Outputs:
	# render
	# Utility:
	# view for about page
	###################################
	intParticipantCount = CustomUser.objects.filter(is_staff = False, is_developer = False).count()
	context = {
		'intTotalParticipantCount': intParticipantCount,
	}
	return render(request,'core/about.html',context = context)

def viewIndex(request):
	###################################
	# Inputs:
	# request
	# Outputs:
	# render
	# Utility:
	# view called for index (home) page
	###################################

	# # get a tip
	# listModelViewedTips = []
	# for modelTip in TipOfDay.objects.all():
	# 	if request.user not in modelTip.responded_users.all():
	# 		# user has not yet responded to tip
	# 		listModelViewedTips.append(modelTip)
	
	# get all their notifications
	qsModelNotificationPost = request.user.recipient_notification_post_set.all().order_by("-pub_date")
	qsModelNotificationHelpRequest = request.user.recipient_notification_help_request_set.all().order_by('-pub_date')
	

	dateToday = date.today()
	strDate = dateToday.strftime("%B %d, %Y")
	# returns 1 for jan first, we want 0 however for indexing
	intDayNum = int(datetime.now().timetuple().tm_yday) - 1
	# use the day num to index the tips
	print(intDayNum)
	modelTipOfDay = get_object_or_404(TipOfDay,day_number=intDayNum)

	context = {
		'strTitle':'index',
		'strDate':strDate,
		'modelTipOfDay':modelTipOfDay,
		'qsModelNotificationPost':qsModelNotificationPost,
		'qsModelNotificationHelpRequest':qsModelNotificationHelpRequest,
	}
	return render(request,'core/index.html',context=context)


@login_required
def viewNotificationDelete(request,notification_type,notification_id):
	###################################
	# Inputs:
	# request, int
	# Outputs:
	# render
	# Utility:
	# view called for delete a notification
	###################################

	# check what type of notification
	if notification_type == "Post":
		modelNotification = get_object_or_404(NotificationPost,id = notification_id)

		if boolModelOwnershipCheck(modelNotification,"recipient",request.user):
			modelNotification.delete()
			messages.success(request,"Notification deleted.")
			return redirect('core:index')
		
	elif notification_type == "HelpRequest":
		modelNotification = get_object_or_404(NotificationHelpRequest,id = notification_id)
		if boolModelOwnershipCheck(modelNotification,"recipient",request.user):
			modelNotification.delete()
			messages.success(request,"Notification deleted.")
			return redirect('core:index')
	
	elif notification_type == "User":
		modelNotification = get_object_or_404(NotificationUser,id = notification_id)
		if boolModelOwnershipCheck(modelNotification,"recipient",request.user):
			modelNotification.delete()
			messages.success(request,"Notification deleted.")
			return redirect('core:index')
	
	else:
		messages.warning(request,"Notification type {} undefined.".format(notification_type))
		return redirect('core:index')

	modelNotification = get_object_or_404(Notification, id = notification_id)
	modelNotificationRecipient = modelNotification.recipient

@login_required
def viewTipRead(request,tip_id):
	# function that reads the tip of day
	# to read a tip we add the user to the tip's responded users,
	# and update the users last tip read date to today

	###########################
	# Inputs:
	# request, id of tip
	###########################
	
	# get the tip
	modelTip = get_object_or_404(TipOfDay,id=tip_id)
	# add to responded users
	if request.user not in modelTip.responded_users.all():
		# add to users
		messages.success(request,"Tip has been read!")
		modelTip.responded_users.add(request.user)
	else:
		messages.success(request,"Tip has been re-read!")

	# regardless of if user has seen tip before, update the 
	# date of last tip read
	today = date.today()
	request.user.last_tip_view_date = today

	return redirect('core:index')

def viewTipArchive(request):

	listModelViewedTips = []

	for modelTip in TipOfDay.objects.all():
		if request.user in modelTip.responded_users.all():
			listModelViewedTips.append(modelTip)

	context = {
		"listModelViewedTips":listModelViewedTips,
	}

	return render(request,'core/tips/archive.html',context=context)