from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

#####################################
# necesssary imports
#####################################
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage

# json
from django.http import JsonResponse
# template loading
from django.template.loader import render_to_string

############################
# Necessary Models
############################

# newsfeed models
from newsfeed.models import HelpRequest,HelpRequestOffer
from core.models import RoomDm

# communities models
from communities.models import Post
# users models
from users.models import CustomUser
##############
# Core models
# notifications, feedback
##############
# notifications
from core.models import (NotificationHelpRequest, 
FeedbackHelpRequestOffer, FeedbackHelpRequestOffer,Dm)

############################
# Necessary Forms
############################
from newsfeed.forms import HelpRequestForm,HelpRequestOfferForm

############################
# Common functions
############################
from newsfeed.common_functions import CommonFunctions

@login_required
def viewIndex(request,page=1):
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
    qsUnfilledHelpRequests = HelpRequest.objects.filter(accepted_user = None).order_by('-pub_date')

    # now we paginate
    intHelpRequestsPerPage = 2
    paginator = Paginator(qsUnfilledHelpRequests,intHelpRequestsPerPage)
    # paginate based on number of help requests
    try:
        qsUnfilledHelpRequests = paginator.page(page)
    except EmptyPage:
        # if exceed limit go to last page
        qsUnfilledHelpRequests = paginator.page(paginator.num_pages)

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
        'qsUnfilledHelpRequests':qsUnfilledHelpRequests,
        "listLastNFollowedUserPosts":listLastNFollowedUserPosts,
        "page":page,
    }

    if request.is_ajax():
        help_requests_html = render_to_string(
            "newsfeed/t/index_help_requests.html",
            {"qsUnfilledHelpRequests":qsUnfilledHelpRequests}
        )
        data = {
            'data_html':help_requests_html,
        }
        return JsonResponse(data)

    return render(request,'newsfeed/index.html',context = context)

@login_required
def viewHelpRequestOfferDetailTag(request, tag):
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
    return render(request,'newsfeed/help_request/detail_tag.html',context)

@login_required
def viewHelpRequestDetail(request,username,slug):
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

    # the offer that was accepted, if present
    modelHelpRequestOfferAccepted = None

    # the offer created by someone who already made an offer, if present
    modelHelpRequestOffer = None

    # get the offer that won, if present
    for modelLoopedOffer in listmodelHelpRequestOffers:
        # each user can only create one help request offer, so only need to check user
        if modelLoopedOffer.author == modelHelpRequest.accepted_user:
            modelHelpRequestOfferAccepted = modelLoopedOffer
        # if request user made offer, show them it
        if modelLoopedOffer.author == request.user:
            modelHelpRequestOffer = modelLoopedOffer

        

    context = {
        "modelHelpRequest":modelHelpRequest,
        "modelHelpRequestAuthor":modelHelpRequestAuthor,

		# if present
        'modelHelpRequestOfferAccepted':modelHelpRequestOfferAccepted,
		# if present
		'modelHelpRequestOffer':modelHelpRequestOffer,

        "listmodelHelpRequestOffers":listmodelHelpRequestOffers,
    }
    return render(request,"newsfeed/help_request/detail.html",context)

@login_required
def viewHelpRequestPrepare(request):
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
def viewHelpRequestDelete(request, username,slug):
    ###################################
    # Inputs:
    # request, username of author, slug of post
    # Outputs:
    # redirect
    # Utility:
    # delete a help request
    ###################################

    modelAuthor = get_object_or_404(CustomUser,username=username)

    modelHelpRequest = get_object_or_404(HelpRequest,author = modelAuthor,slug=slug)
    modelHelpRequestAuthor = modelHelpRequest.author

    if(request.user == modelHelpRequestAuthor):
        messages.success(request,"Help Request successfully deleted.")
        modelHelpRequest.delete()

    return redirect(reverse("newsfeed:index",kwargs={'page':1}))

@login_required
def viewHelpRequestCreate(request):
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
        # NOTE: 
        # at moment just filtering for active users
        for modelLoopedUser in CustomUser.objects.filter(is_active = True):
            # dont send yourself a notification
            if modelLoopedUser != request.user:
                modelNotificationToLoopedUser = NotificationHelpRequest(sender=request.user,recipient=modelLoopedUser,
                    text = "{} created help request \"{}\". See if you can help!".format(request.user.username,strTitle)
                )
                # associate with a help request
                modelNotificationToLoopedUser.help_request = modelCreatedHelpRequest
                # save the notification
                modelNotificationToLoopedUser.save()


        return redirect(reverse('newsfeed:index',kwargs={"page":1}))

def viewHelpRequestOfferCreate(request,username,slug):
    modelAuthor = get_object_or_404(CustomUser,username=username)
    modelHelpRequest = get_object_or_404(HelpRequest, author=modelAuthor,slug=slug)

    # make sure that the help request author
    # is not the same person giving themselves advice!
    if request.user == modelHelpRequest.author:
        messages.warning(request,"Cannot give yourself an offer to help.")
        return redirect(reverse("newsfeed:help-request-detail",kwargs={'username':modelHelpRequest.author,'slug':modelHelpRequest.slug}))
    
    # make sure they have not already made a request
    for modelOffer in modelHelpRequest.help_request_offer_set.all():
        if request.user == modelOffer.author:
            messages.warning(request, "You have already created an offer to help. If you would like to create another, you must remove the old one.")
            return redirect(reverse("newsfeed:help-request-detail",kwargs={'username':modelHelpRequest.author,'slug':modelHelpRequest.slug}))

    if request.method == "POST":

        formHelpRequestOfferForm = HelpRequestOfferForm()
        # commit = false so can edit attributes
        modelCreatedHelpRequestOffer = formHelpRequestOfferForm.save(commit=False)
        
        # edit attributes
        # give an author
        modelCreatedHelpRequestOffer.author = request.user
        # give it its text
        strTextContent = request.POST['text']
        # test if text is valid
        if strTextContent == "":
            # can't have empty text
            messages.warning(request,"You help offer needs to have text present. Please try again.")
            return redirect(reverse("newsfeed:help-request-detail",kwargs={'username':modelHelpRequest.author,'slug':modelHelpRequest.slug}))

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
    
    return redirect(reverse("newsfeed:help-request-detail",kwargs={'username':modelHelpRequest.author,'slug':modelHelpRequest.slug}))

def viewHelpRequestOfferDetail(request,username,slug,id):
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

    return render(request,"newsfeed/help_request/offer/detail.html",context = context)

def viewHelpRequestOfferAccept(request,username,slug,id):
    ###############################
    # Inputs:
    # request, username (of the help request), slug (of the help request),
    # id (of the help request OFFER)
    # Utility:
    # accepts the offer for help and deletes the offer, marks the request as fulfilled
    # deletes all other offers as well
    # 
    # ALSO: Creates the RoomDm where all Dm's between
    # the user who requested help and the user who
    # has offered help can speak
    ###############################

    # get the help request offer
    modelHelpRequestOffer = get_object_or_404(HelpRequestOffer,id=id)
    # get the user who offered
    modelUserOfferer = modelHelpRequestOffer.author
    # get the user who created the help request
    modelUserRequestee = get_object_or_404(CustomUser,username=username)
    # get the help request
    modelHelpRequest = get_object_or_404(HelpRequest,author=modelUserRequestee,slug=slug)
    

    CommonFunctions.voidHelpRequestOfferAccept(modelHelpRequest, modelUserOfferer)

    context = {
        "modelUserOfferer":modelUserOfferer,
        "modelHelpRequest":modelHelpRequest,
    }

    return render(request,'newsfeed/help_request/offer/accept.html',context=context)

def viewHelpRequestOfferReject(request,username,slug,id):
    ###############################
    # Inputs:
    # request, username (of the help request), slug (of the help request),
    # id (of the help request OFFER)
    # Utility:
    # DOES NOT DELETE THE HELP REQUEST OFFER
    # Just a screen so that the user can then fill a form explaining
    # why they want to remove the offer
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
        "modelHelpRequestOffer":modelHelpRequestOffer
    }
    
    return render(request,'newsfeed/help_request/offer/reject.html',context=context)

def viewHelpRequestOfferDelete(request, username, slug,id):
    ###############################
    # Inputs:
    # request, username (of the help request), slug (of the help request),
    # id (of the help request OFFER)
    # Utility:
    # Deletes the help request offer
    ###############################

    # actually deletes the help request offer
    modelHelpRequestAuthor = get_object_or_404(CustomUser,username=username)
    modelHelpRequest = get_object_or_404(HelpRequest,slug=slug,author=modelHelpRequestAuthor)
    modelHelpRequestOffer = get_object_or_404(HelpRequestOffer,id=id)

    # this tests if the user who is deleting is the help request author
    if request.method == "POST" and request.user == modelHelpRequest.author:

        FEEDBACK_CHOICES = [0,1,2,3]

        intFeedbackId = int(request.POST['feedback-id'])

        # if the user screws something up
        if intFeedbackId not in FEEDBACK_CHOICES:
            messages.warning(request,"Feedback id error. Please try resubmitting the form.")
            return redirect(reverse("newsfeed:help-request-offer-detail",kwargs={"username":username,"slug":slug,"id":id}))
        
        # get the feedback
        # this could be done more easily, still learning django feedback choices

        # check if entered text
        # if not, return none
        strText = request.POST.get("text",None)

        modelFeedback = FeedbackHelpRequestOffer(sender=request.user,
            feedback_choice = intFeedbackId ,text=strText
        )
        # save to db
        modelFeedback.save()

        # make sure no user is accepted
        if modelHelpRequest.accepted_user != None:
            modelHelpRequest.accepted_user = None

        #send notification to user that offer rejected
        modelNotification = NotificationHelpRequest(sender=request.user,recipient=modelHelpRequestOffer.author,
            text="Your help request for request \"{}\" has been rejected.".format(modelHelpRequest.title)
        )
        modelNotification.help_request = modelHelpRequest 
        modelNotification.save()

        # delete the offer
        CommonFunctions.voidDeleteHelpRequestOffer(modelHelpRequestOffer)

        messages.success(request,'Help request offer successfully deleted')
        return redirect(reverse("newsfeed:help-request-detail",kwargs={"username":username,"slug":slug}))

    # can also delete if you are the author of the offer
    if request.user == modelHelpRequestOffer.author:
        # make sure no user is accepted
        modelHelpRequest.accepted_user = None
        # save the model!
        modelHelpRequest.save()

        # delete the offer
        CommonFunctions.voidDeleteHelpRequestOffer(modelHelpRequestOffer)

        messages.success(request,"Successfully deleted offer.")
        return redirect(reverse("newsfeed:help-request-detail",kwargs={"username":username,"slug":slug}))

    else:
        messages.warning(request,'You are not able to delete this offer.')
        return redirect(reverse("newsfeed:help-request-detail",kwargs={"username":username,"slug":slug}))
    
@login_required
def viewHelpRequestAcceptedUserResetPrepare(request, username,slug):
    ###############################
    # Inputs:
    # request, username (of the help request), slug (of the help request)
    # Utility:
    # Shows a screen for user to fill out a form on why they wish
    # to reset the help request user
    # When form filled, help request user is reset
    ###############################
    # actually deletes the help request offer
    modelHelpRequestAuthor = get_object_or_404(CustomUser,username=username)
    modelHelpRequest = get_object_or_404(HelpRequest,slug=slug,author=modelHelpRequestAuthor)

    # check if has permission
    if request.user != modelHelpRequestAuthor:
        messages.warning(request,"You do not have permission to do that action.")
        return redirect(reverse("newsfeed:help-request-detail",kwargs={"username":username,"slug":slug}))

    # check if there is an accepted user
    if modelHelpRequest.accepted_user == None:
        messages.warning(request,"There is no accepted user to reject.")
        return redirect(reverse("newsfeed:help-request-detail",kwargs={"username":username,"slug":slug}))

    else:
        context = {
            "modelHelpRequest":modelHelpRequest,
        }
        return render(request,"newsfeed/help_request/accepted_user_reset_prepare.html",context=context)


def viewHelpRequestArchiveDetail(request):
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
    return render(request,'newsfeed/help_request/archive.html',context = context)


######################################
# views for creating dms between users
######################################

def viewDmDetail(request,sender_username,recipient_username,room_name):

    return render("newsfeed/help_request/rooms/dm_detail.html")