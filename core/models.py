from django.db import models
###########################
# Necessary imports
###########################
from django.utils import timezone

###########################
# Necessary other models
###########################
from users.models import CustomUser
from communities.models import Post
from newsfeed.models import HelpRequest,HelpRequestOffer

##########################################
# Dj url imports
##########################################
from django.urls import reverse

# slugs
from django.template.defaultfilters import slugify


# Create your models here.

####################################
#
# Tip of days
#
####################################
class TipOfDay(models.Model):
	# number of the day of the year
	day_number = models.IntegerField()
	# text in the tip of the day
	text = models.CharField(max_length=300,null=False)
	# tag is a comma delimited string
	tags = models.CharField(max_length = 500,null=True,blank=True)
	# users who have responded to tip of day
	responded_users = models.ManyToManyField(CustomUser,related_name="tip_set")

	strDelim = "$"

	def __str__(self):
		return "Tip #{}: {}".format(self.day_number,self.text)
	
	def listGetParsedTags(self):
		if self.tags:
			return [i for i in self.tags.split(self.strDelim)]
		else:
			return []
	
	def reverseGetReadUrl(self):
		# returns a reverse url for the read function of tip
		return reverse('core:tip-read',kwargs={'tip_id':self.id})
	
	def reverseGetArchiveUrl(self):
		# returns url for archive of tips
		return reverse('core:tip-archive',kwargs = {"pg_prev_tips":1})

#######################################
# 
# Models for user feedback
# user feedback is used to improve the site
# 
#######################################

# abstract class for user feedback
# we inherit from this class in order to provide specific types of feedback
class BaseFeedback(models.Model):
	# don't always need text
	pub_date = models.DateTimeField(default=timezone.now)

	class Meta:
		abstract = True

# feedback from a help request, NOT OFFER
# most used when rejecting help request
class FeedbackHelpRequest(BaseFeedback):
	# associated with user, or anonymous (User == null)
	sender = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,related_name = "feedback_help_request_set")
	OFFENSIVE = 0
	INAPPROPRIATE = 1
	NO_REASON = 2
	OTHER = 3

	FEEDBACK_CHOICES = [
		(OFFENSIVE,"offensive"),
		(INAPPROPRIATE,"inappropriate"),
		(NO_REASON,"no reason"),
		(OTHER,"other"),
	]

	# if reason was "other", then text is present
	text = models.CharField(max_length=300,null=True,blank=True)
	feedback_choice = models.CharField(
		max_length=2,choices = FEEDBACK_CHOICES
		,null=True,blank=True)
	
	def __str__(self):
		return "Sender: {}|Id: {}".format(self.sender,self.feedback_choice)
	

# feedback from a help request offer
# most used when rejecting help request offer
class FeedbackHelpRequestOffer(BaseFeedback):
	# associated with user, or anonymous (User == null)
	sender = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,related_name = "feedback_help_request_offer_set")

	OFFENSIVE = 0
	INAPPROPRIATE = 1
	NO_REASON = 2
	OTHER = 3

	FEEDBACK_CHOICES = [
		(OFFENSIVE,"offensive"),
		(INAPPROPRIATE,"inappropriate"),
		(NO_REASON,"no reason"),
		(OTHER,"other"),
	]

	# if reason was "other", then text is present
	text = models.CharField(max_length=300,null=True,blank=True)
	feedback_choice = models.CharField(
		max_length=2,choices = FEEDBACK_CHOICES
		,null=True,blank=True)
	
	def __str__(self):
		return "Sender: {}|Id: {}".format(self.sender,self.feedback_choice)

	
#######################################
# 
# Models for Dm rooms
# Dm rooms are to contain dms, so that 
# a user could have multiple dm conversations 
# with a different users for different reasons
# 
#######################################

class BaseRoom(models.Model):
	# when room created
	pub_date = models.DateTimeField(default=timezone.now)
	# each room has a name / topic
	name = models.CharField(max_length=300)

	slug = models.SlugField(null=False)

	class Meta:
		abstract = True
	
	def save(self,*args,**kwargs):
		# NOTE:
		# if allow users to change the name, may 
		# need to change the slug as well.
		# need to overwrite save to have slug updated when save
		if not self.id:
			self.slug = slugify(self.name)
		super(BaseRoom,self).save(*args,**kwargs)

# room to hold direct messages	
class RoomDm(BaseRoom):
	# a dm room requires both an author and a partner to be complete.

	# person who created room
	author = models.ForeignKey(CustomUser,on_delete = models.CASCADE,related_name="room_dm_author_set",null=False)
	# person who author talks to
	partner= models.ForeignKey(CustomUser,on_delete = models.CASCADE,related_name="room_dm_partner_set",null=False)

	class Meta:
		unique_together = [['author','name']]
	
	def __str__(self):
		return "Author:{}|Partner:{}|Name:{}".format(self.author.username,self.partner.username,self.name)
	
	def reverseGetDetail(self):
		return reverse('newsfeed:help-request-dm-detail',
			kwargs = {'hr_author_username':self.author.username,
			'hr_accepted_user_username':self.partner.username,
			'room_name':self.name,
			})

#######################################
# 
# Models for Dms
# All Dm's must be associated with a "room".
# A room is created for each conversation.
# 
#######################################

# if room == null, then regular dm between two users
class Dm(models.Model):
	# sender
	sender = models.ForeignKey(CustomUser,on_delete = models.CASCADE,related_name = "dm_sender_set")
	# recipient
	recipient = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name = "dm_recipient_set")
	# when it was sent
	pub_date = models.DateTimeField(default=timezone.now)

	# what room it belongs to
	room = models.ForeignKey(RoomDm, on_delete = models.CASCADE,related_name="dm_set",null=True)

	text = models.TextField()


	def __str__(self):
		return self.text
	
	def boolIsReply(self):
		if(self.parent):
			return True
		return False
	
	def reverseGetDetail(self):
		# if has a room, go to help request
		if self.room != None:
			return reverse('newsfeed:help-request-dm-detail',
			kwargs = {'hr_author_username':self.room.author.username,
			'hr_accepted_user_username':self.room.partner.username,
			'room_name':self.room.name,
			})
		# else go to generic dm
		else:
			return reverse('users:dm-detail',kwargs={"username":self.sender.username})
	

#######################################
# 
# Models for Notifications
# All notifications inherit from a base
# 
#######################################

# create a base notification class
class BaseNotification(models.Model):
	text = models.CharField(max_length=300,null=False)
	read = models.BooleanField(default=False)
	pub_date = models.DateTimeField(default=timezone.now)

	class Meta:
		abstract = True

#############
# NOTE:
# Related names are a field in a db, so cannot have the same name even if inherited class
#############

# notifications for post
class NotificationPost(BaseNotification):
	# notification linking to post
	sender = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,related_name = "sender_notification_post_set")
	recipient = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="recipient_notification_post_set",null=False)

	post = models.ForeignKey(Post,on_delete = models.CASCADE,related_name = "notification_post_set")

	def __str__(self):
		return "To: {}|From: {}|Post:{}".format(self.sender,self.recipient,self.post.title)
	
	def strGetType(self):
		# get the type of notification, useful for looping
		return "Post"

class NotificationHelpRequest(BaseNotification):
	# notification linking to help request
	sender = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,related_name = "sender_notification_help_request_set")
	recipient = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="recipient_notification_help_request_set",null=False)

	help_request = models.ForeignKey(HelpRequest,on_delete=models.CASCADE,related_name = "notification_help_request_set")

	def __str__(self):
		return "To: {}|From: {}|HelpRequest:{}".format(self.recipient,self.sender,self.help_request.title)
	
	def strGetType(self):
		return "HelpRequest"	

class NotificationDm(BaseNotification):
	# notification linking to dm
	sender = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,related_name = "sender_notification_dm_set")
	recipient = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="recipient_notification_dm_set",null=False)

	dm = models.ForeignKey(Dm,on_delete = models.CASCADE,related_name = "notification_dm_set")

	def __str__(self):
		return "To: {}|From: {}|Dm:{}".format(self.recipient,self.sender,self.dm)

	def strGetType(self):
		return "Dm"

class NotificationUser(BaseNotification):
	# notification linking to user
	sender = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,related_name = "sender_notification_user_set")
	recipient = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="recipient_notification_user_set",null=False)

	user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="notification_user_set")

	def __str__(self):
		return "To: {}|From: {}|User:{}".format(self.recipient,self.sender,self.user.username)
	
	def strGetType(self):
		return "User"