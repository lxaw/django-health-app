from django.shortcuts import render, redirect

# forms
from .forms import UserRegisterForm

# messages on registration / log in
from django.contrib import messages

# Create your views here.

def viewRegister(request):

	if request.method == "POST":
		# if get post request, instantiate form with user data
		form = UserRegisterForm(request.POST)

		if form.is_valid():
			# save the user
			form.save()

			username = form.cleaned_data.get('username')

			messages.success(request, "Account created for {}. You may now log in.".format(username))
			# redirect to this page after creation of account
			return redirect('users:login')

	else:
		form = UserRegisterForm()

	context = {
		'formRegistration':form,
	}

	return render(request,'users/register.html',context=context)

def viewProfile(request):

	user = request.user

	###################
	# These types may not be correct.
	# ie: I do not know how HTML treats bools
	###################

	context = {
		"dictUserStats" :{
			"strEmail": user.email,
			"strUsername":user.username,
			"strAbout": user.text_about,
			"boolIsPodPlusMember":user.is_pod_plus_member,
			"intPoints":user.int_points,
			"intDaysActive":user.int_days_active,
			"intUsersHelped":user.int_users_helped,
			"strDateJoined":user.date_joined,
		}
	}

	return render(request,'users/profile.html',context = context)