from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import BlogForm, CommentForm
from .models import BlogPost,Comment
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
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


class AddLike(LoginRequiredMixin, View):
    def post(self,request,pk,*args,**kwargs):
        post = BlogPost.objects.get(pk=pk)
        is_dislike = False
        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            post.dislikes.remove(request.user)

        is_like = False
        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            post.likes.add(request.user)

        if is_like:
            post.likes.remove(request.user)

        next = request.POST.get('next','/')
        return HttpResponseRedirect(next)



class AddDislike(LoginRequiredMixin, View):
    def post(self,request,pk,*args,**kwargs):
        post = BlogPost.objects.get(pk=pk)
        is_like = False
        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break
                
        if is_like:
            post.likes.remove(request.user)

        is_dislike = False
        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            post.dislikes.add(request.user)

        if is_dislike:
            post.dislikes.remove(request.user)

        next = request.POST.get('next','/')
        return HttpResponseRedirect(next)