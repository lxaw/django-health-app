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
from .forms import PostForm, CommentForm,HelpRequestForm
#####################################
# Outside imports
#####################################
from django.utils import timezone


@login_required
def viewIndex(request):
	modelPost = Post()

	# note that create post is handled in a different view
	# we use form action to create the objects
	formPostForm = PostForm(instance=modelPost)
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
def viewLikePost(request,post_id):
	modelPost = get_object_or_404(Post,id=post_id)

	if(modelPost.user_likes.filter(id=request.user.id).exists()):
		modelPost.user_likes.remove(request.user)
	else:

		modelPost.user_likes.add(request.user)
		# notify that they liked post
		modelNotificationToReply = Notification(sender=request.user,recipient=modelPost.author, message="{} has liked your post \"{}\".".format(request.user.username,modelPost.title))
		# dont keep showing notification if press like and unlike 
		
		modelNotificationToReply.save()
	
	return redirect('communities:index')

@login_required
def viewPostDetail(request, slug,username):
	modelPostAuthor = get_object_or_404(CustomUser, username=username)
	modelPost = get_object_or_404(Post,slug=slug,author=modelPostAuthor)

	# filter only those comments that are not replies
	listmodelComments = modelPost.comments.filter(active = True).order_by("pub_date")

	# form for creating a comment
	formCommentForm = CommentForm()

	context = {
		"modelPost":modelPost,
		"listmodelComments":listmodelComments,
		"formCommentForm":formCommentForm,
	}
	return render(request, 'communities/post_detail.html',context)

@login_required
def viewProfile(request, username):
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
					modelNotificationToReply = Notification(sender=request.user,recipient=modelParentObj.author, message="{} has replied to your comment.".format(request.user.username))
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
			
			modelNotificationToParent.save()

			# increment the user's notification count

	#return redirect(reverse("communities:post_detail",kwargs = {'username':modelPost.author.username,'slug':modelPost.slug}))
	return redirect('communities:index')

@login_required
def viewDeletePost(request,post_id):
	modelPost = get_object_or_404(Post, id = post_id)
	modelPostAuthor = modelPost.author

	if request.user == modelPostAuthor:
		messages.success(request, "Post successfully deleted.")
		modelPost.delete()
	
	return redirect('communities:index')

@login_required
def viewDeleteComment(request,comment_id):
	modelComment = get_object_or_404(Comment,id = comment_id)
	modelParentPost = modelComment.post
	modelCommentAuthor = modelComment.author

	if request.user == modelCommentAuthor:
		messages.success(request,"Comment successfully deleted.")
		modelComment.delete()

	return redirect(reverse("communities:post_detail",kwargs = {'username':modelParentPost.author.username,'slug':modelParentPost.slug}))

@login_required
def viewAddRemoveFollow(request, username):
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


	return redirect('communities:index')


@login_required
def viewRequestHelp(request):


	context = {
		"formCreateHelpRequest":HelpRequestForm,
	}

	return render(request, "communities/request_help.html",context)

