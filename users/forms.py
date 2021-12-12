from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.models import User


#############################
# Related models
#############################
from .models import CustomUser
from food.models import Food


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
		fields = ("email",)

class CustomUserChangeForm(UserChangeForm):
	###################################
	# Form to change items in custom user
	###################################

	class Meta:
		model = CustomUser
		fields = ("email",)

#############################
# Forms for Foods
#############################

class FoodForm(forms.ModelForm):
	###################################
	# Form to create food object
	###################################

	class Meta:
		model = Food

		# what fields can alter in form
		fields = [
			"kcals",
			"name",
		]
		widgets = {
			'kcals':forms.TextInput(attrs={'cols':5,'rows':20,'placeholder':"Input a value."},)
		}

		exclude = ()