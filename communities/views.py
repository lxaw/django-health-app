from django.contrib.auth.decorators import login_required

#####################################
# HTML routing imports
#####################################
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
# templates
from django.template.loader import render_to_string
# json / serializers
from django.http import JsonResponse

#####################################
# django utils
#####################################
# messages
from django.contrib import messages
# time zones
from django.utils import timezone
# pagination
from django.core.paginator import Paginator, EmptyPage

#####################################
# Necessary models
#####################################
from users.models import CustomUser
from .models import Post,Comment
# notifications
from core.models import NotificationPost, NotificationUser

#####################################
# Necessary forms
#####################################
from .forms import PostForm, CommentForm
from newsfeed.forms import HelpRequestForm

# note! (08/14/22)
# rqeuest.is_ajax has recently be depreciated.
# since this is an archive, here is a new function to replace it.
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required
def viewIndex(request,page=1):
	###################################
	# Inputs:
	# request, page for pagination
	# Outputs:
	# render
	# Utility:
	# view called for index
	###################################


	# note that create post is handled in a different view
	# we use form action to create the objects
	formPostForm = PostForm()
	formCommentForm = CommentForm()

	
	# order the posts
	# Create a dictionary of {Post:Post comments sorted}
	qsPosts = Post.objects.order_by('-pub_date')

	intPostsPerPage = 3
	# paginate based on number of posts
	paginator = Paginator(qsPosts,intPostsPerPage)	

	try:
		qsPosts = paginator.page(page)
	except EmptyPage:
		# if exceed limit go to last page
		qsPosts = paginator.page(paginator.num_pages)

	context = {
		"qsPosts":qsPosts,
		"formPostForm":formPostForm,
		"formCommentForm":formCommentForm,
	}
	# NOTE!
	# request.is_ajax() is depreciated in newer versions of django
	if is_ajax(request):
		posts_html = render_to_string(
			"communities/t/posts.html",
			{'qsPosts':qsPosts}
		)
		data = {
			'posts_html':posts_html,
			'has_next':qsPosts.has_next()
		}
		return JsonResponse(data)

	return render(request,'communities/index.html',context = context)

@login_required
def viewPostPrepare(request):
	context = {

	}

	return render(request,'communities/post_prepare.html',context=context)

@login_required
def viewPostCreate(request):
	###################################
	# Inputs:
	# request
	# Outputs:
	# redirect
	# Utility:
	# view called to create a post
	###################################
	modelPost = Post()

	formPostForm = PostForm(instance=modelPost)

	if request.method == "POST":

		# fill with post data
		formPostForm = PostForm(request.POST)

		modelCreatedPost = formPostForm.save(commit=False)

		formPostForm = PostForm(request.POST)

		if formPostForm.is_valid():
			# save the object
			user = request.user

			modelCreatedPost.author = user

			modelCreatedPost.save()

			# show message that post created
			messages.success(request, "Post created.")

			# redirect
			return redirect(reverse('communities:index',kwargs={"page":1}))
	
	context = {
		"formPostForm":formPostForm,
	}
	return redirect(reverse('communities:index',kwargs={"page":1}))

@login_required
def viewLikeUnlikePost(request,post_id):
	###################################
	# Inputs:
	# request, int
	# Outputs:
	# redirect
	# Utility:
	# view to like or unlike a post
	###################################
	modelPost = get_object_or_404(Post,id=post_id)

	if(modelPost.user_likes.filter(id=request.user.id).exists()):
		modelPost.user_likes.remove(request.user)
	else:

		modelPost.user_likes.add(request.user)

		################
		# Create a notification.
		# populate all fields
		################

		# notify that they liked post
		modelNotificationPost = NotificationPost()
		# give sender
		modelNotificationPost.sender = request.user
		# give recipient
		modelNotificationPost.recipient = modelPost.author
		# link to post
		modelNotificationPost.post = modelPost
		# give text
		modelNotificationPost.text = "{} has liked your post {}.".format(request.user,modelPost.title)
		
		modelNotificationPost.save()
	
	return redirect(reverse('communities:index',kwargs={"page":1}))

@login_required
def viewPostDetail(request, slug,username):
	###################################
	# Inputs:
	# request, str slug, str username
	# Outputs:
	# render
	# Utility:
	# view for see post by user
	###################################
	modelPostAuthor = get_object_or_404(CustomUser, username=username)
	modelPost = get_object_or_404(Post,slug=slug,author=modelPostAuthor)

	# filter only those comments that are not replies
	listmodelComments = modelPost.comments.filter(active = True).order_by("pub_date")

	# form for creating a comment
	formCommentForm = CommentForm()

	context = {
		"modelPost":modelPost,
		"listPostComments":listmodelComments,
		"formCommentForm":formCommentForm,
	}
	return render(request, 'communities/post_detail.html',context)

@login_required
def viewProfile(request, username,page=1):
	###################################
	# Inputs:
	# request, str username, page for pagination
	# Outputs:
	# render
	# Utility:
	# view called for public profile
	###################################

	modelUser = get_object_or_404(CustomUser, username = username)
	qsPosts = modelUser.created_post_set.order_by('-pub_date')

	# pagination number of posts per page
	intPostsPerPage = 3
	# paginate based on number of posts
	paginator = Paginator(qsPosts,intPostsPerPage)

	try:
		qsPosts = paginator.page(page)
	except EmptyPage:
		# if exceed limit go to last page
		qsPosts = paginator.page(paginator.num_pages)

	context = {
		"modelViewedUser": modelUser,
		"qsPosts":qsPosts,
	}

	return render(request, "communities/profile.html",context)

############
# Creating comments
# With reference to:
# https://stackoverflow.com/questions/44837733/how-to-make-add-replies-to-comments-in-django
############
@login_required
def viewCreateComment(request,username,slug):
	###################################
	# Inputs:
	# request, str username, str slug
	# Outputs:
	# redirect
	# Utility:
	# view to create comments (or replies)
	###################################
	# get the author
	modelPostAuthor = get_object_or_404(CustomUser,username = username)
	# get the post
	modelPost = get_object_or_404(Post, slug = slug,author = modelPostAuthor)

	if request.method == "POST":
		# get the current user
		modelUser = request.user

		# form for comment
		formCommentForm = CommentForm(data=request.POST)

		if formCommentForm.is_valid():
			modelParentObj = None
			# try to get parent comment id from hidden input
			try:
				intParentId = int(request.POST.get("intParentId"))
			except:
				intParentId = None
			# if parent has been submitted get the parent's id
			if intParentId:
				modelParentObj = Comment.objects.get(id=intParentId)
				# if there exists a parent
				if modelParentObj:
					# create reply
					modelReplyComment = formCommentForm.save(commit=False)
					# put user with comment
					modelReplyComment.author = modelUser
					# put the parent id in the reply
					modelReplyComment.parent = modelParentObj
					# since reply, notify the person you reply to
					modelNotificationToReply = NotificationPost()
					modelNotificationToReply.sender = request.user
					modelNotificationToReply.recipient = modelParentObj.author
					modelNotificationToReply.text = "{} has replied to your comment on post {}.".format(request.user.username,modelPost.title)
					modelNotificationToReply.post = modelPost
					modelNotificationToReply.save()

			# Else, this is a normal comment
			# create but dont save to db
			modelNewComment = formCommentForm.save(commit = False)
			modelNewComment.post = modelPost
			modelNewComment.author = modelUser
			# save
			modelNewComment.save()

			# create a notification for the other users
			# always notify the post owner
			modelNotificationToParent = NotificationPost()
			modelNotificationToParent.sender = request.user
			modelNotificationToParent.recipient = modelPost.author
			modelNotificationToParent.text= "{} has commented on your post {}.".format(request.user.username,modelPost.title)
			modelNotificationToParent.post = modelPost
			modelNotificationToParent.save()
		# if form not valid, show message
		else:
			messages.warning(request,"Message could not be sent. Please try again.")
			

	return redirect(reverse('communities:post-detail',kwargs={'username':modelPost.author.username,'slug':modelPost.slug}))

@login_required
def viewPostDelete(request,post_id):
	###################################
	# Inputs:
	# request, int
	# Outputs:
	# redirect
	# Utility:
	# view to delete posts
	###################################
	modelPost = get_object_or_404(Post, id = post_id)
	modelPostAuthor = modelPost.author

	###########
	# always check if the user that is calling the function is the user who owns the thing
	###########
	if request.user == modelPostAuthor:
		modelPost.delete()
	
	return redirect(reverse('communities:index',kwargs={"page":1}))

@login_required
def viewDeleteComment(request,comment_id):
	###################################
	# Inputs:
	# request, int
	# Outputs:
	# HttpResponseRedirect
	# Utility:
	# view to delete comments
	###################################
	modelComment = get_object_or_404(Comment,id = comment_id)
	modelParentPost = modelComment.post
	modelCommentAuthor = modelComment.author

	if request.user == modelCommentAuthor:
		modelComment.delete()

	return redirect(reverse("communities:post-detail",kwargs = {'username':modelParentPost.author.username,'slug':modelParentPost.slug}))

@login_required
def viewAddRemoveFollow(request, username):
	###################################
	# Inputs:
	# request, str username
	# Outputs:
	# HttpResponseRedirect
	# Utility:
	# add or remove follow a user
	###################################
	modelUserToBeFollowed = get_object_or_404(CustomUser,username=username)

	modelCurrentUser = request.user

	if modelCurrentUser != modelUserToBeFollowed:
		if modelUserToBeFollowed not in modelCurrentUser.follows.all():
			# follow
			modelCurrentUser.follows.add(modelUserToBeFollowed)
		else:
			# unfollow
			modelCurrentUser.follows.remove(modelUserToBeFollowed)

	# this never runs if use ajax
	return HttpResponseRedirect('/')

@login_required
def viewLeaderboardIndex(request):
	if not request.user.is_pod_plus_member:
		messages.warning(request,"Only POD+ members may access this page.")
		return redirect("communities:index")
	
	# else they are a member
	context = {

	}

	return render(request,'communities/leaderboard.html',context=context)