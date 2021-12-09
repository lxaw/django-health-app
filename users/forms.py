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
	email = forms.EmailField()

	class Meta:
		model = CustomUser
		fields = ['username','email','phone_number','password1','password2']



class CustomUserCreationForm(UserCreationForm):

	class Meta:
		model = CustomUser
		fields = ("email",)

class CustomUserChangeForm(UserChangeForm):

	class Meta:
		model = CustomUser
		fields = ("email",)

#############################
# Forms for Foods
#############################

class FoodForm(forms.ModelForm):

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