
from django import forms
#####################################
# Necessary models
#####################################
from .models import HelpRequest, HelpRequestOffer

class HelpRequestForm(forms.ModelForm):
	class Meta:
		model = HelpRequest

		fields = [
			"title",
			"text",
			"tags",
		]
		exclude = ()

class HelpRequestOfferForm(forms.ModelForm):
	class Meta:
		model = HelpRequestOffer

		fields = [
			"text",
		]

		exclude = ()