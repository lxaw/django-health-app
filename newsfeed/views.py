from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

# Create your views here.

############################
# Necessary Models
############################

from newsfeed.models import HelpRequest
from communities.models import Post
from users.models import CustomUser

@login_required
def viewIndex(request):

    # list of all recent posts
    listRecentPosts = []
    for modelPost in Post.objects.all().order_by('-pub_date'):
        if modelPost.boolWithinXDays(1) and modelPost.author != request.user:
            listRecentPosts.append(modelPost)
    
    # list of unfilled help requests
    # right now it has every single request, in reality may want to limit
    listUnfilledHelpRequests = []
    for modelHelpRequest in HelpRequest.objects.all().order_by("-pub_date"):
        if not modelHelpRequest.boolWasRespondedTo():
            listUnfilledHelpRequests.append(modelHelpRequest)


    context = {
        "listRecentPosts":listRecentPosts,
        "listUnfilledHelpRequests":listUnfilledHelpRequests,
    }
    return render(request,'newsfeed/index.html',context = context)

@login_required
def viewDetailByTag(request, tag):

    # list of unfilled help requests
    # right now it has every single request, in reality may want to limit
    listUnfilledHelpRequests = []
    for modelHelpRequest in HelpRequest.objects.all().order_by("-pub_date"):
        if not modelHelpRequest.boolWasRespondedTo() and (tag in modelHelpRequest.get_parsed_tags()):
            listUnfilledHelpRequests.append(modelHelpRequest)
    context = {
        "strSelectedTag":tag,
        "listUnfilledHelpRequests":listUnfilledHelpRequests,
    }
    return render(request,'newsfeed/help_request_detail_by_tag.html',context)

@login_required
def viewDetail(request,username,slug):
    # View an individual help request
    modelHelpRequestAuthor = get_object_or_404(CustomUser,username = username)
    modelHelpRequest = get_object_or_404(HelpRequest,slug=slug,author=modelHelpRequestAuthor)

    context = {
        "modelHelpRequest":modelHelpRequest,
        "modelHelpRequestAuthor":modelHelpRequestAuthor,
    }
    return render(request,"newsfeed/help_request_detail.html",context)
    