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

##########################################
# Other models
##########################################
from users.models import CustomUser


##########################################
# Models related to posts
##########################################

class Post(models.Model):
	# associate with user
	author = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name = "created_post_set")
	# associate with a title
	title = models.CharField(max_length=200,null=False)
	# associate with text
	text = models.CharField(max_length = 300)

	# store date of publication
	pub_date = models.DateTimeField(default=timezone.now)

	# associate with the users that have commented / posted / whatever
	responded_users = models.ManyToManyField(CustomUser)

	# associate with likes
	user_likes = models.ManyToManyField(CustomUser, related_name="user_likes")

	# slug field
	slug = models.SlugField(null=False)

	# for deactivating inappropriate comments
	active = models.BooleanField(default=True)

	class Meta:
		unique_together = [['author','title']]

	def save(self, *args, **kwargs):
		if not self.id:
			# newly created obj, so set slug
			self.slug = slugify(self.title)

		super(Post,self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('communities:post-detail',kwargs={"slug":self.slug,
			"username":self.author.username}
			)
	
	def intGetLikeCount(self):
		return self.user_likes.count()

	def boolWithinXDays(self,intDays):
		now = timezone.now()

		return now - datetime.timedelta(days=intDays) <= self.pub_date <= now
	
	def __str__(self):
		return self.title

class Comment(models.Model):
	# associate with post
	post = models.ForeignKey(Post, on_delete = models.CASCADE,related_name="comments")
	# associate with user
	author = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
	
	text = models.TextField()

	pub_date = models.DateTimeField(default=timezone.now)

	# for deactivating inappropriate comments
	active = models.BooleanField(default = True)

	# if comment on other comments
	parent = models.ForeignKey('self',null=True, blank = True, related_name = 'replies',on_delete=models.CASCADE)

	class Meta:
		# sort by time created
		ordering = ('pub_date',)
	
	def __str__(self):
		return "Comment by {}".format(self.author.username)

	def boolIsReply(self):
		if(self.parent):
			return True
		return False