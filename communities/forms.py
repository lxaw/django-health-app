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
			"text",
		]
		exclude = ()

		# change size of form
		widgets = {
			'text':forms.Textarea(attrs={'rows':10,'cols':50,
			'style':'resize:none'}),
		}

# Form for creating Comments
class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = [
			'text',
		]
		widgets = {
			'text':forms.Textarea(attrs={'rows':2,'cols':20,
			'style':'resize:none'}),
		}
