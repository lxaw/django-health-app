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

	# get a tip
	listModelTips = []
	for modelTip in TipOfDay.objects.all():
		if request.user not in modelTip.responded_users.all():
			# user has not yet responded to tip
			listModelTips.append(modelTip)
	
	# get all their notifications
	qsModelNotificationPost = request.user.recipient_notification_post_set.all().order_by("-pub_date")
	

	dateToday = date.today()
	strDate = dateToday.strftime("%B %d, %Y")

	context = {
		'strTitle':'index',
		'strDate':strDate,
		'modelTip':listModelTips,
		'qsModelNotificationPost':qsModelNotificationPost,
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

	
