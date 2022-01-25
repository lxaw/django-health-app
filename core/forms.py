# forms for models
from django import forms

#############################
# Related models
#############################
from .models import Dm

#############################
# forms for Dms
#############################
class DmForm(forms.ModelForm):
	# form to create a dm
	class Meta:
		model = Dm

		fields = [
			'text',
		]
		exclude = ()