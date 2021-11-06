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
	author = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
	# associate with a title
	title = models.CharField(max_length=200,unique=True,null=False)
	# associate with text
	text_content = models.CharField(max_length = 300)

	# store date of publication
	pub_date = models.DateTimeField(default=timezone.now)

	# associate with the users that have commented / posted / whatever
	responded_users = models.ManyToManyField(CustomUser,related_name='responded_users_set')

	# associate with likes
	user_likes = models.ManyToManyField(CustomUser, related_name="user_likes")

	# slug field
	slug = models.SlugField(null=False)

	def save(self, *args, **kwargs):
		if not self.id:
			# newly created obj, so set slug
			self.slug = slugify(self.title)

		super(Post,self).save(*args, **kwargs)



	def get_absolute_url(self):
		return reverse('post_detail',kwargs={"slug":self.slug,
			"username":self.author.username}
			)
	
	def like_count(self):
		return self.user_likes.count()

	def boolWithinXDays(self,intDays):
		now = timezone.now()

		return now - datetime.timedelta(days=intDays) <= self.date <= now
	
	def __str__(self):
		return self.title