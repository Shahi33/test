from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import BlogForm, CommentForm
from .models import BlogPost,Comment
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.contrib.auth import get_user_model
from .forms import UserCreate
from django.contrib.auth.models import User
# Create your views here.

def home(request):

    context = {
        'blog': BlogPost.objects.all(),
        'comment':Comment.objects.all(),
        
    }
    return render(request,"post/home.html", context)

@login_required
def adminHome(request):
    User = get_user_model()
    users = User.objects.all()
    context = {
        'blog': BlogPost.objects.all(),
        'comment':Comment.objects.all(),
        'users':users
    }
    return render(request,"post/adminHome.html", context)


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
    return redirect('post:adminHome')

@login_required
def comment(request,id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.author=request.user
            form_obj.blog=BlogPost.objects.get(id = id)
            form_obj.save()  
            next = request.POST.get('next','/')
            return HttpResponseRedirect(next)
        else:
            form = CommentForm(instance=request.user)
            args = {'form':'form'}
        next = request.POST.get('next','/')
        return HttpResponseRedirect(next)


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


def singleBlog(request,id):
    if request.user.is_superuser:
        post = BlogPost.objects.get(id = id)
        
    else:
        post = BlogPost.objects.get(id = id )
        if not post.approved:
            post = None

    context = {
        'post': post,
        'comment':Comment.objects.filter(blog = post),
    }
    return render(request,"post/singleBlog.html", context)


# create user

def createUser(request):
    register_form = UserCreate()
    if request.method == 'POST':
        register_form = UserCreate(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data.get("username")
            first_name = register_form.cleaned_data.get("first_name")
            last_name = register_form.cleaned_data.get("last_name")
            email = register_form.cleaned_data.get("username")
            password = register_form.cleaned_data.get("password1")
            is_superuser = register_form.cleaned_data.get("is_superuser")
            
            
            new_user = User.objects.create_user(username, email, password, first_name=first_name,last_name=last_name, is_superuser=is_superuser)

            return redirect('post:adminHome')
    # context = {'register_form':register_form,}
    # return render(request,"users/register.html",context)

@login_required
def block(request, id):
    if request.user.is_superuser:
        block = User.objects.get(id=id)
        if block.is_active:
            block.is_active = False
        else:
            block.is_active = True
        block.save()
    return redirect('post:adminHome')


@login_required
def delete(request, id):
    if request.user.is_superuser:
        user = User.objects.get(id=id)
        user.delete()
        
    return redirect('post:adminHome')

@login_required
def postDelete(request, id):
    if request.user.is_superuser:
        post = BlogPost.objects.get(id=id)
        post.delete()
        
    return redirect('post:adminHome')