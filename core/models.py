from django.db import models
###########################
# Necessary imports
###########################
from django.utils import timezone

###########################
# Necessary other models
###########################
from users.models import CustomUser

# Create your models here.


class TipOfDay(models.Model):
	text_content = models.CharField(max_length=300,null=False)

	# tag is a comma delimited string
	tags = models.CharField(max_length = 500)

	# users who have responded to tip of day
	responded_users = models.ManyToManyField(CustomUser,related_name="responded_users")

	def __str__(self):
		return "Tip #{}: {}".format(self.id,self.text_content)


