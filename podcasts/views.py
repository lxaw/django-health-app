from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def viewIndex(request):
	###################################
	# Inputs:
	# request
	# Outputs:
    # render
	# Utility:
	# Delete a food item
    # Index view for the podcast page
    ###################################
    context = {

    }
    return render(request,'podcasts/index.html',context = context)