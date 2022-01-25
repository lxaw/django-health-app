###########################
# Django functions
###########################
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# paginator
from django.core.paginator import Paginator, EmptyPage

# json
from django.http import JsonResponse
# templates
from django.template.loader import render_to_string

###########################
# Necessary models
###########################
from .models import (TipOfDay,NotificationPost,NotificationDm,
NotificationHelpRequest,NotificationUser)
from users.models import CustomUser

###########################
# Necessary imports
###########################
from datetime import date
from datetime import datetime
import random

from core.base_functions import boolModelOwnershipCheck

# Create your views here.

def viewAbout(request):
	###################################
	# Inputs:
	# request
	# Outputs:
	# render
	# Utility:
	# view for about page
	###################################
	intParticipantCount = CustomUser.objects.filter(is_staff = False, is_developer = False).count()
	context = {
		'intTotalParticipantCount': intParticipantCount,
	}
	return render(request,'core/about.html',context = context)

# n prepend = notificiation
# pg = page for paginatiron
def viewIndex(request,pg_post=1,pg_help_req=1,pg_dm=1):
	###################################
	# Inputs:
	# request, page number for posts, page num for help reqs, page num for dms
	# Outputs:
	# render
	# Utility:
	# view called for index (home) page
	###################################

	# get all their notifications
	qsNotifPosts = request.user.recipient_notification_post_set.order_by("-pub_date")
	qsNotifHelpRequests = request.user.recipient_notification_help_request_set.order_by('-pub_date')
	qsNotifDms = request.user.recipient_notification_dm_set.order_by('-pub_date')


	dateToday = date.today()
	strDate = dateToday.strftime("%B %d, %Y")
	# returns 1 for jan first, we want 0 however for indexing
	intDayNum = int(datetime.now().timetuple().tm_yday) - 1
	# use the day num to index the tips
	modelTipOfDay = get_object_or_404(TipOfDay,day_number=intDayNum)

	# pagination
	intPostNotifsPerPage = 3
	intHelpRequestNotifsPerPage = 3
	intDmNotifsPerPage = 3

	paginator_post = Paginator(qsNotifPosts,intPostNotifsPerPage)
	paginator_hr = Paginator(qsNotifHelpRequests,intHelpRequestNotifsPerPage)
	paginator_dm = Paginator(qsNotifDms,intDmNotifsPerPage)

	try:
		qsNotifPosts = paginator_post.page(pg_post)
	except EmptyPage:
		qsNotifPosts = paginator_post.page(paginator_post.num_pages)
	
	try:
		qsNotifHelpRequests = paginator_hr.page(pg_help_req)
	except EmptyPage:
		qsNotifHelpRequests = paginator_hr.page(paginator_hr.num_pages)
	
	try:
		qsNotifDms = paginator_dm.page(pg_dm)
	except EmptyPage:
		qsNotifDms = paginator_dm.page(paginator_dm.num_pages)
	

	context = {
		'strTitle':'index',
		'strDate':strDate,
		'modelTipOfDay':modelTipOfDay,
		'qsNotifPosts':qsNotifPosts,
		'qsNotifHelpRequests':qsNotifHelpRequests,
		'qsNotifDms':qsNotifDms,

		# page numbers
		'intNotifPostPgNum':pg_post,
		'intNotifHrPgNum':pg_help_req,
		'intNotifDmPgNum':pg_dm,
	}
	return render(request,'core/index.html',context=context)
@login_required
def aGetNotifDms(request,pg_post,pg_help_req,pg_dm):
	###########################
	# Inputs:
	# request, str of model type, int for pg of posts, int for page of
	# help reqs, int for page of dms
	###########################
	# ajax view to get the models for index

	intPerPage = 3

	# get all post notifications in order
	qsNotifDms = request.user.recipient_notification_dm_set.all().order_by("-pub_date")
	# paginate
	paginator = Paginator(qsNotifDms,intPerPage)

	try:
		qsNotifDms = paginator.page(pg_dm)
	except EmptyPage:
		qsNotifDms = paginator.page(paginator.num_pages)

	html_data = render_to_string(
		"core/t/index_dms.html",
		{"qsNotifDms":qsNotifDms,
		# page numbers
		"intNotifDmPgNum":pg_post,
		'intNotifHrPgNum':pg_help_req,
		"intNotifDmPgNum":pg_dm,
		}
	)	
	data = {
		"html_data":html_data,
	}
	return JsonResponse(data)

@login_required
def aGetNotifPosts(request,pg_post,pg_help_req,pg_dm):
	###########################
	# Inputs:
	# request, str of model type, int for pg of posts, int for page of
	# help reqs, int for page of dms
	###########################
	# ajax view to get the models for index

	intPerPage = 3

	# get all post notifications in order
	qsNotifPosts = request.user.recipient_notification_post_set.all().order_by("-pub_date")
	# paginate
	paginator = Paginator(qsNotifPosts,intPerPage)

	try:
		qsNotifPosts = paginator.page(pg_post)
	except EmptyPage:
		qsNotifPosts = paginator.page(paginator.num_pages)

	html_data = render_to_string(
		"core/t/index_posts.html",
		{"qsNotifPosts":qsNotifPosts,
		# page numbers
		"intNotifPostPgNum":pg_post,
		'intNotifHrPgNum':pg_help_req,
		"intNotifDmPgNum":pg_dm,
		}
	)	
	data = {
		"html_data":html_data,
	}
	return JsonResponse(data)

@login_required
def aGetNotifHelpRequests(request,pg_post,pg_help_req,pg_dm):
	###########################
	# Inputs:
	# request, str of model type, int for pg of posts, int for page of
	# help reqs, int for page of dms
	###########################
	# ajax view to get the models for index

	intPerPage = 3

	# get all post notifications in order
	qsNotifHelpRequests = request.user.recipient_notification_help_request_set.all().order_by("-pub_date")
	# paginate
	paginator = Paginator(qsNotifHelpRequests,intPerPage)

	try:
		qsNotifHelpRequests = paginator.page(pg_help_req)
	except EmptyPage:
		qsNotifHelpRequests = paginator.page(paginator.num_pages)
	

	html_data = render_to_string(
		"core/t/index_help_requests.html",
		{"qsNotifHelpRequests":qsNotifHelpRequests,
		# page numbers
		"intNotifPostPgNum":pg_post,
		'intNotifHrPgNum':pg_help_req,
		"intNotifDmPgNum":pg_dm,
		}
	)	
	data = {
		"html_data":html_data,
	}
	return JsonResponse(data)



@login_required
def viewNotificationDelete(request,notification_type,notification_id):
	###################################
	# Inputs:
	# request, int
	# Outputs:
	# render
	# Utility:
	# view called for delete a notification
	###################################

	# check what type of notification
	if notification_type == "Post":
		modelNotification = get_object_or_404(NotificationPost,id = notification_id)

		if boolModelOwnershipCheck(modelNotification,"recipient",request.user):
			modelNotification.delete()
			messages.success(request,"Notification deleted.")
			return redirect(reverse('core:index',args=[1,1,1]))
		
	elif notification_type == "HelpRequest":
		modelNotification = get_object_or_404(NotificationHelpRequest,id = notification_id)
		if boolModelOwnershipCheck(modelNotification,"recipient",request.user):
			modelNotification.delete()
			messages.success(request,"Notification deleted.")
			return redirect(reverse('core:index',args=[1,1,1]))
	
	elif notification_type == "User":
		modelNotification = get_object_or_404(NotificationUser,id = notification_id)
		if boolModelOwnershipCheck(modelNotification,"recipient",request.user):
			modelNotification.delete()
			messages.success(request,"Notification deleted.")
			return redirect(reverse('core:index',args=[1,1,1]))
	
	elif notification_type == "Dm":
		modelNotification = get_object_or_404(NotificationDm,id = notification_id)
		if boolModelOwnershipCheck(modelNotification,"recipient",request.user):
			modelNotification.delete()
			messages.success(request,"Notification deleted.")
			return redirect(reverse('core:index',args=[1,1,1]))

	
	else:
		messages.warning(request,"Notification type {} undefined.".format(notification_type))
		return redirect(reverse('core:index',args=[1,1,1]))

	modelNotification = get_object_or_404(Notification, id = notification_id)
	modelNotificationRecipient = modelNotification.recipient

@login_required
def viewTipRead(request,tip_id):
	# function that reads the tip of day
	# to read a tip we add the user to the tip's responded users,
	# and update the users last tip read date to today

	###########################
	# Inputs:
	# request, id of tip
	###########################
	
	# get the tip
	modelTip = get_object_or_404(TipOfDay,id=tip_id)
	# add to responded users
	if request.user not in modelTip.responded_users.all():
		# add to users
		messages.success(request,"Tip has been read!")
		modelTip.responded_users.add(request.user)
	else:
		messages.success(request,"Tip has been re-read!")

	# regardless of if user has seen tip before, update the 
	# date of last tip read
	today = date.today()
	request.user.last_tip_view_date = today
	# need to save user after
	request.user.save()

	return redirect(reverse('core:index',args=[1,1,1]))

@login_required
def viewTipArchive(request,pg_prev_tips):
	# inputs:
	# request, page for the previous tip

	intPerPage = 3

	qsModelViewedTips = request.user.tip_set.all()
	# paginator
	paginator = Paginator(qsModelViewedTips,intPerPage)

	try:
		qsModelViewedTips = paginator.page(pg_prev_tips)
	except EmptyPage:
		qsModelViewedTips = paginator.page(paginator.num_pages)

	context = {
		"qsModelViewedTips":qsModelViewedTips,
	}

	return render(request,'core/tips/archive.html',context=context)

@login_required
def aGetTips(request,pg_prev_tips):
	# inputs:
	# request, int pg

	intPerPage = 3

	qsTips = request.user.tip_set.all()

	# paginate
	paginator = Paginator(qsTips,intPerPage)

	try:
		qsTips = paginator.page(pg_prev_tips)
	except EmptyPage:
		qsTips = paginator.page(paginator.num_pages)

	html_data = render_to_string(
		"core/tips/t/archived_tips.html",
		{"qsModelViewedTips":qsTips}
	)
	data = {
		"html_data":html_data,
	}

	return JsonResponse(data)