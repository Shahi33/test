from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, unique=True)
    content = models.TextField()
    approved = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, blank = True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank = True, related_name='dislikes')

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(BlogPost, related_name = "comments", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=200)
    
    def __str__(self):
        return self.comment


