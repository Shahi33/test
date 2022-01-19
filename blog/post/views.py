from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import BlogForm, CommentForm
from .models import BlogPost,Comment
# Create your views here.
def home(request):
    context = {
        'blog': BlogPost.objects.all(),
        'comment':Comment.objects.all(),
    }
    return render(request,"post/home.html", context)

@login_required
def createBlog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            from_obj = form.save(commit=False)
            from_obj.author=request.user
            from_obj.save()  
            return redirect('post:home')
        else:
            form = BlogForm(instance=request.user)
            args = {'form':'form'}
        return redirect('post:home')

@login_required
def approveBlog(request,id):
    blog = BlogPost.objects.get(id = id)
    if blog.approved:
        blog.approved = False
    else:
        blog.approved = True

    blog.save()
    return redirect('post:home')

@login_required
def comment(request,id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.author=request.user
            form_obj.blog=BlogPost.objects.get(id = id)
            form_obj.save()  
            return redirect('post:home')
        else:
            form = CommentForm(instance=request.user)
            args = {'form':'form'}
        return redirect('post:home')