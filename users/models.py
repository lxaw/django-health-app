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

# for resizing images
from PIL import Image

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
	
	# img path
	DEFAULT_PROF_PIC_PATH = "users/profile_pics/defaults/default_profile_pic.jpg"
	PROF_PIC_UPLOAD_PATH = "users/profile_pics"
	
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
	is_pod_plus_member= models.BooleanField(default = False)

	int_points = models.IntegerField(default = 0)	
	int_users_helped = models.IntegerField(default = 0)
	int_days_active = models.IntegerField(default = 0)

	about = models.TextField(gettext_lazy(
		'about'),max_length=500,blank = True)

	# need Pillow library for images
	profile_picture = models.ImageField(default=DEFAULT_PROF_PIC_PATH,upload_to=PROF_PIC_UPLOAD_PATH)

	# store when the user joined
	date_joined = models.DateTimeField(default=timezone.now)

	# for following users
	follows = models.ManyToManyField('CustomUser',related_name='followed_by')
	
	# Defining that we use a custom account manager
	objects = CustomUserManager()

	# store user phone number
	phone_number = models.CharField(max_length=12,unique=True,null=False)

	# store if they responded to tip of day
	# to check if they viewed the one for today, compare the last 
	# view date to today's date
	last_tip_view_date = models.DateField(null=True, blank=True)

	# USERNAME_FIELD is the default unique field that ID's user
	# This is the unique field that identies users.
	USERNAME_FIELD = "username"
	REQUIRED_FIELDS = ["email","phone_number"]

	def boolViewedTodaysTip(self):
		# check if viewed today's tip
		# when view a tip, it updates the last date view to that
		# of the day you are viewing
		if self.last_tip_view_date == datetime.date.today():
			return True
		return False

	def set_user_profile_picture_default(self):
		# deletes and sets prof pic to default

		# delete old picture
		self.profile_picture.delete(save=False)
		# set default
		self.profile_picture = self.DEFAULT_PROF_PIC_PATH
		# save
		self.save_no_img_change()
	
	def save_no_img_change(self,*args,**kwargs):
		super().save(*args,**kwargs)


	def save(self,*args,**kwargs):
		##############
		# TO DO:
		# Delete old images when a user uploads new ones
		##############
		max_height = 300
		max_width = 300

		# NOTE: Should be a way to check if only one field changed
		# delete and reset prof pic
		# run save method of parent class
		super().save(*args,**kwargs)

		# delete the last image
		
		# resize image
		img = Image.open(self.profile_picture.path)
		if img.height > max_height or img.width > max_width:
			output_size = (max_height,max_width)
			img.thumbnail(output_size)
			img.save(self.profile_picture.path)

		

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
		return reverse('communities:profile',kwargs={"username":self.username,"page":1})
	
	def get_notification_count(self):
		# returns the integer amount of all notifications
		# that a user has
		
		# check each notification type, get sum
		intSum = 0
		
		intSum += (self.recipient_notification_help_request_set.count() +
		self.recipient_notification_post_set.count())

		return intSum
		