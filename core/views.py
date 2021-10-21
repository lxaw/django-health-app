from django.shortcuts import render

from django.http import HttpResponse

from users.models import CustomUser

# Create your views here.

def viewAbout(request):
	context = {

	}
	return render(request,'core/about.html',context = context)

def viewIndex(request):

	intParticipantCount = CustomUser.objects.filter(is_staff = False, is_developer = False).count()

	print(intParticipantCount)

	context = {
		'strTitle':'index',
		'intTotalParticipantCount': intParticipantCount,
		'strUpdates': 'Test',
	}

	return render(request,'core/index.html',context = context)