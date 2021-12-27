from django import forms

# models
from .models import Food

#############################
# Forms for Foods
#############################
class FoodForm(forms.ModelForm):
	###################################
	# Form to create food object
	###################################

	class Meta:
		model = Food

		# what fields can alter in form
		fields = [
			"kcals",
			"name",
		]
		widgets = {
			'kcals':forms.TextInput(attrs={'cols':5,'rows':20,'placeholder':"Input a value."},)
		}

		exclude = ()