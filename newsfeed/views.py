from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
#####################################
# Messages
#####################################
from django.contrib import messages

############################
# Necessary Models
############################

# core models
from core.models import Notification

# newsfeed models
from newsfeed.models import HelpRequest

# communities models
from communities.models import Post
# users models
from users.models import CustomUser

############################
# Necessary Forms
############################
from newsfeed.forms import HelpRequestForm

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

@login_required
def viewRequestHelp(request):

	return render(request, "newsfeed/request_help.html")

# delete help request
@login_required
def viewDeleteHelpRequest(request, id):
	modelHelpRequest = get_object_or_404(HelpRequest,id=id)
	modelHelpRequestAuthor = modelHelpRequest.author

	if(request.user == modelHelpRequestAuthor):
		messages.success(request,"Help Request successfully deleted.")
		modelHelpRequest.delete()

	return redirect("newsfeed:index")

@login_required
def viewCreateHelpRequest(request):
	# This is a list of all possible tags in the create help request form
	listPossibleTags = ["nutrition","diet","routine"]

	if request.method == "POST":
		# get the user who wants help
		modelUser = request.user
		# get title for post
		strTitle = request.POST['title']
		# get the content
		strTextContent = request.POST['text_content']

		# get the tags and concat them
		strConcatedTags = ""
		for strPossibleTag in listPossibleTags:
			if strPossibleTag in request.POST.keys():
				strConcatedTags += (strPossibleTag) + "-"
		if(strConcatedTags != ""):
			# if not empty, remove the last "-"
			strConcatedTags = strConcatedTags[:-1]

		# create help request form so we can create object
		formCreateHelpRequest = HelpRequestForm()
		# commit = false so we can edit attributes	
		modelCreatedHelpRequest = formCreateHelpRequest.save(commit = False)
		# edit attributes
		modelCreatedHelpRequest.author = modelUser
		modelCreatedHelpRequest.title = strTitle
		modelCreatedHelpRequest.text_content = strTextContent
		# if tags, put them
		if strConcatedTags != "":
			modelCreatedHelpRequest.tags = strConcatedTags

		# save the model when all attributes edited
		modelCreatedHelpRequest.save()

		# create an alert for all users
		# do we want to do this? Or just for certain users?
		for modelLoopedUser in CustomUser.objects.all():
			modelNotificationToLoopedUser = Notification(sender=request.user,recipient=modelLoopedUser,
				message = "{} created help request \"{}\". See if you can help!".format(request.user.username,strTitle)
			)
			modelNotificationToLoopedUser.save()



	return redirect('newsfeed:index')
    