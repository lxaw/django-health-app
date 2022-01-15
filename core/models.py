from django.db import models
###########################
# Necessary imports
###########################
from django.utils import timezone

###########################
# Necessary other models
###########################
from users.models import CustomUser, DirectMessage
from communities.models import Post
from newsfeed.models import HelpRequest,HelpRequestOffer

##########################################
# Dj url imports
##########################################
from django.urls import reverse

# Create your models here.

#####################################
# Models for notification
#####################################

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

class NotificationDirectMessage(BaseNotification):
	# notification linking to dm
	sender = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,related_name = "sender_notification_direct_message_set")
	recipient = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="recipient_notification_direct_message_set",null=False)

	direct_message = models.ForeignKey(DirectMessage,on_delete = models.CASCADE,related_name = "notification_direct_message_set")

	def __str__(self):
		return "To: {}|From: {}|DM:{}".format(self.recipient,self.sender,self.direct_message)

	def strGetType(self):
		return "DirectMessage"

class NotificationUser(BaseNotification):
	# notification linking to user
	sender = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,related_name = "sender_notification_user_set")
	recipient = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="recipient_notification_user_set",null=False)

	user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="notification_user_set")

	def __str__(self):
		return "To: {}|From: {}|User:{}".format(self.recipient,self.sender,self.user.username)
	
	def strGetType(self):
		return "User"
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

# feedback from a help request offer
# most used when rejecting help request
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
	feedback_chocies = models.CharField(
		max_length=2,choices = FEEDBACK_CHOICES
		,null=True,blank=True)

	


