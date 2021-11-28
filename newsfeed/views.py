from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

############################
# Necessary Models
############################

from communities.models import Post, Comment

@login_required
def viewIndex(request):

    listRecentPosts = []
    for modelPost in Post.objects.all().order_by('-pub_date'):
        if modelPost.boolWithinXDays(1) and modelPost.author != request.user:
            listRecentPosts.append(modelPost)


    context = {
        "listRecentPosts":listRecentPosts,
    }
    return render(request,'newsfeed/index.html',context = context)
    