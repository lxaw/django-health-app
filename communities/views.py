#####################################
# dj default imports
#####################################
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

from users.models import CustomUser

#####################################
# Necessary models
#####################################

from .models import Post

#####################################
# Necessary forms
#####################################
from .forms import PostForm
#####################################
# Outside imports
#####################################
from django.utils import timezone

@login_required
def viewIndex(request):
	listModelPosts = Post.objects.all()


	context = {
		"listModelPosts":listModelPosts,
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
	return render(request, 'communities/create_post.html',context)

@login_required
def viewLikePost(request,post_id):
	modelPost = get_object_or_404(Post,id=post_id)

	if(modelPost.user_likes.filter(id=request.user.id).exists()):
		modelPost.user_likes.remove(request.user)
	else:
		modelPost.user_likes.add(request.user)
	
	return redirect('communities:index')

@login_required
def viewPostDetail(request, slug,username):
	postAuthor = get_object_or_404(CustomUser, username=username)
	modelPost = get_object_or_404(Post,slug=slug,author=postAuthor)

	context = {
		"modelPost":modelPost,
	}
	return render(request, 'communities/post_detail.html',context)

@login_required
def viewProfile(request, username):
	modelUser = get_object_or_404(CustomUser, username = username)

	context = {
		"strUsername":modelUser.username,
		"intUsersHelped":modelUser.int_users_helped,
		"intDaysActive":modelUser.int_days_active,
		"strDateJoined":modelUser.date_joined,
		"strAbout":modelUser.text_about,
	}

	return render(request, "communities/profile.html",context)
