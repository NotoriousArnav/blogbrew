from django import forms

class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Add your comment...'}))
