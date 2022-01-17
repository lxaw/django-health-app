###########################
# Django imports
###########################
from django.db import models

from django.utils import timezone
# get text lazy allows at any point you think data may be translated into user's lang
from django.utils.translation import gettext_lazy

from django.urls import reverse

# import models
from users.models import CustomUser

###########################
# Non-django imports
###########################
import datetime

###########################
# Food models
###########################

class Food(models.Model):
    name = models.CharField(max_length=300)
    # the user that uploaded the food
    author = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="uploaded_meals")
    # the amount of kilocals
    kcals = models.FloatField()
    # the date at which the meal was uploaded
    pub_date = models.DateTimeField(default=timezone.now)

    def boolWithinXDays(self,intDays):
        # check to see if the upload of the meal is within
        # intDays of today

        # get the current time
        now = timezone.now()
        return now - datetime.timedelta(days=intDays) <= self.date <= now
    
    def __str__(self):
        # string function for printing
        return "Name: {}\nKcals:{}".format(self.name,self.kcals)