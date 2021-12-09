from django.db import models
###########################
# Necessary imports
###########################
from django.utils import timezone

###########################
# Necessary other models
###########################
from users.models import CustomUser

##########################################
# Dj url imports
##########################################
from django.urls import reverse

# Create your models here.

class Notification(models.Model):
	sender = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,related_name = "sender_notification")
	recipient = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="recipient_notification",null=False)
	message = models.TextField(null=False)
	read = models.BooleanField(default=False)
	pub_date = models.DateTimeField(default=timezone.now)
	# if you ever need to link to some model for urls
	# store the related name for the reverse
	related_reverse = models.CharField(max_length=300,null=True)
	# store any arguments for the reverse
	related_reverse_args = models.CharField(max_length=300,null=True)

	def __str__(self):
		return "Sender {} | Recipient: {}".format(self.sender,self.recipient)
	
	def get_parsed_reverse_args(self):
		return self.related_reverse_args.split("$")
	
	def get_absolute_url(self):
		return reverse(self.related_reverse,args=self.get_parsed_reverse_args())

class TipOfDay(models.Model):
	text_content = models.CharField(max_length=300,null=False)

	# tag is a comma delimited string
	tags = models.CharField(max_length = 500)

	# users who have responded to tip of day
	responded_users = models.ManyToManyField(CustomUser,related_name="responded_users")

	def __str__(self):
		return "Tip #{}: {}".format(self.id,self.text_content)
