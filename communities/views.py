from django.contrib.auth.decorators import login_required

#####################################
# HTML routing imports
#####################################
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

#####################################
# Messages
#####################################
from django.contrib import messages


#####################################
# Necessary models
#####################################
from users.models import CustomUser
from core.models import Notification
from .models import Post,Comment

#####################################
# Necessary forms
#####################################
from .forms import PostForm, CommentForm
from newsfeed.forms import HelpRequestForm
#####################################
# Outside imports
#####################################
from django.utils import timezone

#####################################
# import reverse dictionary to use reverses 
# more easily for notifications
#####################################
from core.notification_reverses.reverses import dictNotificationReverses

@login_required
def viewIndex(request):
	###################################
	# Inputs:
	# request
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
	dictModelPosts = {}
	for modelPost in Post.objects.all().order_by('-pub_date'):
		dictModelPosts[modelPost] = modelPost.comments.filter(active=True).order_by("pub_date")

	context = {
		"dictModelPosts":dictModelPosts,
		"formPostForm":formPostForm,
		"formCommentForm":formCommentForm,
	}

	return render(request,'communities/index.html',context = context)

@login_required
def viewCreatePost(request):
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
			return redirect('communities:index')
	
	context = {
		"formPostForm":formPostForm,
	}
	return redirect("communities:index")

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
		# notify that they liked post
		modelNotification = Notification(sender=request.user,recipient=modelPost.author, message="{} has liked your post \"{}\".".format(request.user.username,modelPost.title))
		################
		# Note:
		# To link to post, need to make sure the url of notification
		# matches how we decide to continue to do urls for posts.
		# This is important as old notifications could give bad urls.
		################
		# building the url
		modelNotification.related_reverse = dictNotificationReverses["communities"]['post']['detail']
		modelNotification.related_reverse_args = "{}${}".format(modelPost.author.username,modelPost.slug)

		# 
		# dont keep showing notification if press like and unlike 
		# 
		
		modelNotification.save()
	
	return redirect('communities:index')

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
def viewProfile(request, username):
	###################################
	# Inputs:
	# request, str username
	# Outputs:
	# render
	# Utility:
	# view called for public profile
	###################################
	modelUser = get_object_or_404(CustomUser, username = username)
	listModelPosts = modelUser.created_post_set.all().order_by("-pub_date")

	context = {
		"modelViewedUser": modelUser,
		"listModelPosts":listModelPosts,
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
					modelNotificationToReply = Notification(sender=request.user,recipient=modelParentObj.author, message="{} has replied to your comment on post \"{}\".".format(request.user.username,modelPost.title))
					modelNotificationToReply.related_reverse = dictNotificationReverses["communities"]["post"]["detail"]
					modelNotificationToReply.related_reverse_args = "{}${}".format(modelPost.author.username,modelPost.slug)

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
			modelNotificationToParent = Notification(sender=request.user,recipient=modelPost.author,
				message="{} has commented on your post \"{}\".".format(request.user.username,modelPost.title))

			# link to a reverse
			modelNotificationToParent.related_reverse = dictNotificationReverses["communities"]["post"]["detail"]
			# give the arguments to the reverse
			modelNotificationToParent.related_reverse_args = "{}${}".format(modelPost.author.username,modelPost.slug)
			
			modelNotificationToParent.save()

	return redirect('communities:index')

@login_required
def viewDeletePost(request,post_id):
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

	if request.user == modelPostAuthor:
		modelPost.delete()
	
	return redirect('communities:index')

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

	return redirect(reverse("communities:post_detail",kwargs = {'username':modelParentPost.author.username,'slug':modelParentPost.slug}))

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
