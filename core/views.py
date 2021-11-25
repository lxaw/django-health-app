###########################
# Django functions
###########################
from django.shortcuts import render
from django.http import HttpResponse

###########################
# Necessary models
###########################
from .models import TipOfDay
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