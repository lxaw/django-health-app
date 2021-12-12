###########################
# Django imports
###########################
from django.db import models

from django.utils import timezone
# get text lazy allows at any point you think data may be translated into user's lang
from django.utils.translation import gettext_lazy

from django.urls import reverse

# import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager

###########################
# Non-django imports
###########################

import datetime

###########################
# Custom user models
# With reference to: 
# https://www.youtube.com/watch?v=Ae7nc1EGv-A
###########################

# PermissionsMixin allows the user class to get the permissions that dj needs

class CustomUserManager(BaseUserManager):

	def create_superuser(self,email,username,password,**other_fields):
		# this is a required field by Django, cannot change name.
		other_fields.setdefault("is_superuser",True)

		##############################################
		# Defaults that run when create superuser
		##############################################
		other_fields.setdefault("is_staff",True)
		other_fields.setdefault("is_active",True)
		other_fields.setdefault("is_developer",True)

		if other_fields.get("is_staff") is not True:
			raise ValueError(
				"Superuser must be assigned to is_staff = True"
			)
		if other_fields.get("is_superuser") is not True:
			raise ValueError(
				"Superuser must be assigned to is_superuser = True"
			)
		
		return self.create_user(email,username,password,**other_fields)

	def create_user(self,email,username,password,phone_number,**other_fields):
		##############################################
		# Function that is called when users are created
		##############################################
		# normalize the email by lowercasing domain part

		if not username:
			raise ValueError(gettext_lazy("Must provide a username."))

		if not email:
			raise ValueError(gettext_lazy("Must provide email address."))
		if not phone_number:
			raise ValueError(gettext_lazy("Must provide phone number."))

		email = self.normalize_email(email)
		user = self.model(email=email,username=username,phone_number=phone_number,**other_fields)

		# set the password
		user.set_password(password)
		# save the instance
		user.save()

		return user

class CustomUser(AbstractBaseUser,PermissionsMixin):
	##############################################
	# User models
	##############################################
	# Authentication of user
	email = models.EmailField(gettext_lazy('email address'),unique = True)
	username = models.CharField(max_length=150,unique = True)

	########################
	# User permissions / boolean traits
	########################
	# permissions

	# Django requirements:
	is_staff = models.BooleanField(default = False)
	########################
	# NOTE: You may want an additional step to authenticate users via 
	# email or something else. At the moment, we assume
	# that they are activated from creation.
	#######################
	is_active = models.BooleanField(default= True)

	########################
	# Custom fields
	########################
	is_developer = models.BooleanField(default = False)
	is_pod_plus_member= models.BooleanField(default = True)

	int_points = models.IntegerField(default = 0)	
	int_users_helped = models.IntegerField(default = 0)
	int_days_active = models.IntegerField(default = 0)

	text_about = models.TextField(gettext_lazy(
		'about'),max_length=500,blank = True)

	# need Pillow library for images
	profile_picture = models.ImageField(default="users/profile_pics/defaults/default_profile_pic.jpg",upload_to="users/profile_pics")

	# store when the user joined
	date_joined = models.DateTimeField(default=timezone.now)

	# for following users
	follows = models.ManyToManyField('CustomUser',related_name='followed_by')
	
	# Defining that we use a custom account manager
	objects = CustomUserManager()

	# store user phone number
	phone_number = models.CharField(max_length=12,unique=True,null=False)

	# USERNAME_FIELD is the default unique field that ID's user
	# This is the unique field that identies users.
	USERNAME_FIELD = "username"
	REQUIRED_FIELDS = ["email","phone_number"]

	def __str__(self):
		###################
		# String function when printing models
		# Default for what shows when a model is displayed
		###################
		return self.username
	
	def get_public_profile_url(self):
		####################################
		# Returns a reverse to the public
		# profile page of a user
		####################################
		return reverse('communities:profile',kwargs={"username":self.username})
