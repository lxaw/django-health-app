from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.

def viewIndex(request):
	context = {
		'strTitle':'index',
		'intTotalParticipantCount': 5,
		'strUpdates': 'Test',
	}

	return render(request,'core/index.html',context = context)