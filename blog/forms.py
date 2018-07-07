#django has 2 base classes to build forms, Form and ModelForm
from .models import Comment
from django import forms

#for email purpose
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                                widget=forms.Textarea)

#for commending purpose
#here create a form from model
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

#to search posts
class SearchForm(forms.Form):
    query = forms.CharField()
