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

			messages.success(request, "Account created for {}".format(username))
			# redirect to this page after creation of account
			return redirect('core:index')

	else:
		form = UserRegisterForm()

	context = {
		'formRegistration':form,
	}

	return render(request,'users/register.html',context=context)