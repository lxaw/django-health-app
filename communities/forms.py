from django import forms


#####################################
# Necessary models
#####################################

from .models import Post
from users.models import CustomUser

class PostForm(forms.ModelForm):
	class Meta:
		model = Post

		# the editable fields by user
		fields = [
			"title",
			"text_content",
		]
		exclude = ()

		# change size of form
		widgets = {
			'text_content':forms.Textarea(attrs={'rows':10,'cols':50}),
		}
