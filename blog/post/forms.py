# from .models import User
from django import forms
from django.contrib.auth.models import User
from post.models import BlogPost,Comment




class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        
        fields = [
            'title','content'
        ]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        
        fields = [
            'comment'
        ]

