# from .models import User
from django import forms
from django.contrib.auth.models import User
from post.models import BlogPost,Comment
from django.contrib.auth.forms import UserCreationForm

class UserCreate(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2','is_superuser']




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

