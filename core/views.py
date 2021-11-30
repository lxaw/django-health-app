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
from .models import TipOfDay, Notification
from users.models import CustomUser

###########################
# Necessary imports
###########################
from datetime import date
import random

# Create your views here.
def viewAbout(request):
	intParticipantCount = CustomUser.objects.filter(is_staff = False, is_developer = False).count()
	context = {
		'intTotalParticipantCount': intParticipantCount,
	}
	return render(request,'core/about.html',context = context)

def viewIndex(request):

	listModelTips = []
	for modelTip in TipOfDay.objects.all():
		if request.user not in modelTip.responded_users.all():
			# user has not yet responded to tip
			listModelTips.append(modelTip)
	

	dateToday = date.today()
	strDate = dateToday.strftime("%B %d, %Y")
	strDayName = dateToday.strftime("%A")

	context = {
		'strTitle':'index',
		'strDate':strDate,
		'strDayName':strDayName,
		'modelTip':listModelTips,
	}

	return render(request,'core/index.html',context = context)

@login_required
def viewDeleteNotification(request,notification_id):
	modelNotification = get_object_or_404(Notification, id = notification_id)
	modelNotificationRecipient = modelNotification.recipient

	if request.user == modelNotificationRecipient:
		messages.success(request, "Notification successfully deleted.")
		modelNotification.delete()
	
	return redirect('core:index')
