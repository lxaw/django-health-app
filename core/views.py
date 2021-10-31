###########################
# Django functions
###########################
from django.shortcuts import render
from django.http import HttpResponse

###########################
# Necessary models
###########################
from users.models import CustomUser

###########################
# Necessary imports
###########################
from datetime import date

# Create your views here.

def viewAbout(request):
	context = {

	}
	return render(request,'core/about.html',context = context)

def viewIndex(request):

	intParticipantCount = CustomUser.objects.filter(is_staff = False, is_developer = False).count()
	dateToday = date.today()
	strDate = dateToday.strftime("%B %d, %Y")
	strDayName = dateToday.strftime("%A")

	context = {
		'strTitle':'index',
		'intTotalParticipantCount': intParticipantCount,
		'strDate':strDate,
		'strDayName':strDayName,
	}

	return render(request,'core/index.html',context = context)