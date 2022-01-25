##########################################
# Default dj imports
##########################################
from django.db import models
from django.utils import timezone

##########################################
# Dj url imports
##########################################
from django.urls import reverse

##########################################
# Dj slugs
##########################################
from django.template.defaultfilters import slugify

##########################################
# Outside libraries
##########################################
import datetime

# Create your models here.

# other needed models
from users.models import CustomUser

##########################################
# Models related to requests for help
##########################################
class HelpRequest(models.Model):
	# associate with user
	author = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name = "created_help_request_set")
	# associate with a title
	title = models.CharField(max_length=200,null=False)
	# associate with text
	text = models.CharField(max_length = 300)
	# associate with tags
	tags = models.CharField(max_length = 300,null=True)

	# store date of publication
	pub_date = models.DateTimeField(default=timezone.now)

	# store date of last accepted user
	accept_date = models.DateTimeField(null=True,blank=True)

	# associate with the user that is to help 
	accepted_user = models.ForeignKey(CustomUser,null=True,blank=True,on_delete=models.CASCADE,related_name = "responded_help_request_set")

	# associate with a room for dm's
	room = models.ForeignKey("core.RoomDm",null=True,on_delete=models.CASCADE,related_name="help_request_set")

	# slug field
	slug = models.SlugField(null=False)

	# delimiter
	delim = "$"

	# what needs to be unique together
	# ie, cannot have user "test" create request titled "help"
	# twice
	class Meta:
		unique_together = [['author','title']]
	
	def boolWasRespondedTo(self):
		return (self.accepted_user != None)
	
	# what to call when save model
	def save(self, *args, **kwargs):
		if not self.id:
			# newly created obj, so set slug
			self.slug = slugify(self.title)

		super(HelpRequest,self).save(*args, **kwargs)

	# return the url associated with it
	# this is the url for viewing the request
	def get_absolute_url(self):
		if self.id:
			return reverse('newsfeed:help-request-detail',kwargs={"slug":self.slug,
				"username":self.author.username}
				)
		else:
			return reverse("")
	
	def get_parsed_tags(self):
		if self.tags:
			return [i for i in self.tags.split(self.delim)]
		else:
			return []

	# check if created within day amount
	def boolWithinXDays(self,intDays):
		now = timezone.now()
		return now - datetime.timedelta(days=intDays) <= self.pub_date <= now
	
	# get a list of all users who offered help
	def listGetOfferedUsers(self):
		listAllUsers = []
		for modelOffer in self.help_request_offer_set.all():
			listAllUsers.append(modelOffer.author)
		
		return listAllUsers
	
	def __str__(self):
		return self.title

##########################################
# Models related to yes no accept requests
##########################################

class HelpRequestOffer(models.Model):
	# associate with user
	author = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="help_request_offer_set")
	# text associated with the message
	text = models.CharField(max_length=300)
	# store date of poub
	pub_date = models.DateTimeField(default=timezone.now)
	# associate with a request for help
	help_request = models.ForeignKey(HelpRequest,on_delete=models.CASCADE,related_name="help_request_offer_set")
	# if accepted go true
	is_accepted = models.BooleanField(default=False)

	def get_absolute_url(self):
		return reverse('newsfeed:help-request-offer-detail',kwargs={'username':self.help_request.author.username,
		"slug":self.help_request.slug,"id":self.id})

	def boolIsAccepted(self):
		# check if someone accepted offer
		return self.is_accepted
	
	def __str__(self):
		return "Help offer by \"{}\" for \"{}\"".format(self.author.username,self.help_request.title)