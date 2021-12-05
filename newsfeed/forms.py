
from django import forms
#####################################
# Necessary models
#####################################
from .models import HelpRequest
class HelpRequestForm(forms.ModelForm):
	class Meta:
		model = HelpRequest

		fields = [
			"title",
			"text_content",
			"tags",
		]
		exclude = ()