from django import forms


#####################################
# Necessary models
#####################################

from .models import Post, Comment

# Form for creating post
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

# Form for creating Comments
class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = [
			'body',
		]
