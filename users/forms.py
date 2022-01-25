from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.models import User


#############################
# Related models
#############################
from .models import CustomUser
from food.models import Food

#############################
# Forms for searching
#############################
class SearchUserForm(forms.Form):
	query = forms.CharField(label="Search",max_length=100)

#############################
# Forms for User Creation / Change
#############################

class UserRegisterForm(UserCreationForm):
	###################################
	# Form to fill when registering users
	###################################
	email = forms.EmailField()

	class Meta:
		# what model to create
		model = CustomUser
		# what fields that are to be filled
		fields = ['username','email','phone_number','password1','password2']



class CustomUserCreationForm(UserCreationForm):
	###################################
	# Form to create a new custom user
	###################################

	class Meta:
		model = CustomUser
		fields = ('username','email','phone_number','password1','password2')

class CustomUserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = CustomUser
		fields = ['username','email','profile_picture','about']

# special bc passwords are hashed
class CustomUserUpdatePasswordForm(forms.ModelForm):
	
	class Meta:
		model = CustomUser
		fields = ['password']