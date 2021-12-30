from django.shortcuts import render

# Create your views here.

def viewFitnessIndex(request):

	context = {

	}
	return render(request,'fitness/index.html',context=context)