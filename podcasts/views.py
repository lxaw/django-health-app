from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def viewIndex(request):
    context = {

    }
    return render(request,'podcasts/index.html',context = context)