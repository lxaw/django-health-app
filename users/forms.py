from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.models import User

from .models import CustomUser


class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = CustomUser
		fields = ['username','email','password1','password2']



class CustomUserCreationForm(UserCreationForm):

	class Meta:
		model = CustomUser
		fields = ("email",)

class CustomUserChangeForm(UserChangeForm):

	class Meta:
		model = CustomUser
		fields = ("email",)