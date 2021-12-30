from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

#####################################
# necesssary imports
#####################################
from django.contrib import messages
from django.utils import timezone

############################
# Necessary Models
############################

# newsfeed models
from newsfeed.models import HelpRequest,HelpRequestOffer

# communities models
from communities.models import Post
# users models
from users.models import CustomUser
# notifications
from core.models import NotificationHelpRequest

############################
# Necessary Forms
############################
from newsfeed.forms import HelpRequestForm,HelpRequestOfferForm

@login_required
def viewIndex(request):
	###################################
	# Inputs:
	# request
	# Outputs:
	# render
	# Utility:
	# view called when go to index page of newsfeed
	###################################

	# variable for how many days 
	intWithinDays = 7

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

	listLastNFollowedUserPosts = []
	# loop thru followed users, get their recent posts
	for modelUser in request.user.follows.all():
		# loop thru their posts
		for modelPost in modelUser.created_post_set.all():
			# if within, append
			if modelPost.boolWithinXDays(intWithinDays):
				listLastNFollowedUserPosts.append(modelPost)

	context = {
        "listRecentPosts":listRecentPosts,
        "listUnfilledHelpRequests":listUnfilledHelpRequests,
		"listLastNFollowedUserPosts":listLastNFollowedUserPosts,
    }
	return render(request,'newsfeed/index.html',context = context)

@login_required
def viewIndexByTag(request, tag):
	###################################
	# Inputs:
	# request, str tag
	# Outputs:
	# render
	# Utility:
	# view called when looking at help requests by tag
	###################################

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
    return render(request,'newsfeed/help_request/help_request_detail_by_tag.html',context)

@login_required
def viewDetailHelpRequest(request,username,slug):
	###################################
	# Inputs:
	# request, str username, str slug
	# Outputs:
	# render
	# Utility:
	# view called when seeing an individual help reqeust
	###################################

    # View an individual help request
    modelHelpRequestAuthor = get_object_or_404(CustomUser,username = username)
    modelHelpRequest = get_object_or_404(HelpRequest,slug=slug,author=modelHelpRequestAuthor)

	# get all the offers
    listmodelHelpRequestOffers = modelHelpRequest.help_request_offer_set.all()

    context = {
        "modelHelpRequest":modelHelpRequest,
        "modelHelpRequestAuthor":modelHelpRequestAuthor,
		"listmodelHelpRequestOffers":listmodelHelpRequestOffers,
    }
    return render(request,"newsfeed/help_request/help_request_detail.html",context)

@login_required
def viewRequestHelp(request):
	###################################
	# Inputs:
	# request
	# Outputs:
	# render
	# Utility:
	# view called when requesting help
	###################################

	return render(request, "newsfeed/request_help.html")

#######################################################
#
# Utility views
#
#######################################################

# delete help request
@login_required
def viewDeleteHelpRequest(request, id):
	###################################
	# Inputs:
	# request, int id
	# Outputs:
	# redirect
	# Utility:
	# delete a help request
	###################################

	modelHelpRequest = get_object_or_404(HelpRequest,id=id)
	modelHelpRequestAuthor = modelHelpRequest.author

	if(request.user == modelHelpRequestAuthor):
		messages.success(request,"Help Request successfully deleted.")
		modelHelpRequest.delete()

	return redirect("newsfeed:index")

@login_required
def viewCreateHelpRequest(request):
	###################################
	# Inputs:
	# request
	# Outputs:
	# render
	# Utility:
	# view called when requesting help
	###################################

	# This is a list of all possible tags in the create help request form
	listPossibleTags = ["nutrition","diet","routine"]

	if request.method == "POST":
		# get the user who wants help
		modelUser = request.user
		# get title for post
		strTitle = request.POST['title']
		# get the content
		strTextContent = request.POST['text']

		# get the tags and concat them
		strConcatedTags = ""
		for strPossibleTag in listPossibleTags:
			if strPossibleTag in request.POST.keys():
				strConcatedTags += (strPossibleTag) + "$"
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
		modelCreatedHelpRequest.text = strTextContent
		# if tags, put them
		if strConcatedTags != "":
			modelCreatedHelpRequest.tags = strConcatedTags

		# save the model when all attributes edited
		modelCreatedHelpRequest.save()

		# create an alert for all users
		# do we want to do this? Or just for certain users?
		for modelLoopedUser in CustomUser.objects.all():
			# dont send yourself a notification
			if modelLoopedUser != request.user:
				modelNotificationToLoopedUser = NotificationHelpRequest(sender=request.user,recipient=modelLoopedUser,
					text = "{} created help request \"{}\". See if you can help!".format(request.user.username,strTitle)
				)
				# associate with a help request
				modelNotificationToLoopedUser.help_request = modelCreatedHelpRequest
				# save the notification
				modelNotificationToLoopedUser.save()

	return redirect('newsfeed:index')

def viewCreateHelpRequestOffer(request,username,slug):
	modelAuthor = get_object_or_404(CustomUser,username=username)
	modelHelpRequest = get_object_or_404(HelpRequest, author=modelAuthor,slug=slug)

	# make sure that the help request author
	# is not the same person giving themselves advice!
	if request.user == modelHelpRequest.author:
		messages.error(request,"Cannot give yourself an offer to help.")
		return redirect("newsfeed:index")

	if request.method == "POST":

		formHelpRequestOfferForm = HelpRequestOfferForm()
		# commit = false so can edit attributes
		modelCreatedHelpRequestOffer = formHelpRequestOfferForm.save(commit=False)
		
		# edit attributes
		# give an author
		modelCreatedHelpRequestOffer.author = request.user
		# give it its text
		strTextContent = request.POST['text']
		modelCreatedHelpRequestOffer.text = strTextContent
		# give it its help request
		modelCreatedHelpRequestOffer.help_request = modelHelpRequest
		# now save
		modelCreatedHelpRequestOffer.save()

		##############
		# Create notification
		##############
		modelNotification = NotificationHelpRequest(sender=request.user,recipient=modelHelpRequest.author,
			text = "{} has offered to help on your help request \"{}\"".format(request.user.username,modelHelpRequest.title)
		)
		modelNotification.help_request = modelHelpRequest

		modelNotification.save()

		# create message
		messages.success(request,"Successfully created help request offer.")
	
	return redirect("newsfeed:index")

def viewDetailHelpRequestOffer(request,username,slug,id):
	###############################
	# Inputs:
	# request, username (of the help request), slug (of the help request),
	# id (of the help request OFFER)
	###############################
	modelHelpRequestOffer = get_object_or_404(HelpRequestOffer,id=id)
	modelHelpRequest = modelHelpRequestOffer.help_request

	context = {
		"modelHelpRequestOffer":modelHelpRequestOffer,
		"modelHelpRequest":modelHelpRequest,
	}

	return render(request,"newsfeed/help_request/help_request_offer_detail.html",context = context)

def viewAcceptHelpRequestOffer(request,username,slug,id):
	###############################
	# Inputs:
	# request, username (of the help request), slug (of the help request),
	# id (of the help request OFFER)
	# Utility:
	# accepts the offer for help and deletes the offer, marks the request as fulfilled
	# deletes all other offers as well
	###############################
	# get the help request offer
	modelHelpRequestOffer = get_object_or_404(HelpRequestOffer,id=id)
	# get the user who offered
	modelUserOfferer = modelHelpRequestOffer.author
	# get the user who created the help request
	modelUserRequestee = get_object_or_404(CustomUser,username=username)
	# get the help request
	modelHelpRequest = get_object_or_404(HelpRequest,author=modelUserRequestee,slug=slug)
	# mark the help request as fulfilled (ie add offerer to responded_users)
	modelHelpRequest.accepted_user = modelUserOfferer
	print('here')
	# # keep track of when it was accepted
	modelHelpRequest.accept_date = timezone.now()
	modelHelpRequest.save()

	context = {
		"modelUserOfferer":modelUserOfferer,
		"modelHelpRequest":modelHelpRequest,
	}

	return render(request,'newsfeed/help_request/help_request_accept.html',context=context)

def viewRejectHelpRequestOffer(request,username,slug,id):
	###############################
	# Inputs:
	# request, username (of the help request), slug (of the help request),
	# id (of the help request OFFER)
	# Utility:
	# rejects the offer by deleting the help reqeust offer. No change to 
	# the original help request
	###############################

	# get the help request offer
	modelHelpRequestOffer = get_object_or_404(HelpRequestOffer,id=id)
	# get the user who offered
	modelUserOfferer = modelHelpRequestOffer.author
	# get the user who created the help request
	modelUserRequestee = get_object_or_404(CustomUser,username=username)
	# get the help request
	modelHelpRequest = get_object_or_404(HelpRequest,author=modelUserRequestee,slug=slug)

	context = {
		"modelUserOfferer":modelUserOfferer,
		"modelHelpRequest":modelHelpRequest,
	}
	
	return render(request,'newsfeed/help_request/help_request_reject.html',context=context)

def viewDetailArchive(request):
	# shows user's old help requests / current ones

	# get the unfulfilled requests
	listmodelPendingRequests = []
	# get the filled help requests
	listmodelAcceptedRequests = []

	# loop thru user's created requests, append to appropriate list
	for modelHelpRequest in request.user.created_help_request_set.all():
		if modelHelpRequest.boolWasRespondedTo():
			# put in responded list
			listmodelAcceptedRequests.append(modelHelpRequest)
		else:
			listmodelPendingRequests.append(modelHelpRequest)

	context = {
		"listmodelPendingRequests": listmodelPendingRequests,
		"listmodelAcceptedRequests": listmodelAcceptedRequests,
	}
	return render(request,'newsfeed/help_request/help_request_archive.html',context = context)