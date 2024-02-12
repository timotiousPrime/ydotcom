# Forms
from django import forms
# Models
from .models import Post


class PostForm(forms.ModelForm):
    class meta:
        model = Post
        fields = ['message']