"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import AddDislike, AddLike
urlpatterns = [
    path('', views.home, name = 'home'),
    
    path('createUser/', views.createUser, name = 'createUser'),
    path('adminHome/', views.adminHome, name = 'adminHome'),
    path('create/', views.createBlog, name = 'createBlog'),
    path('approve/<id>/', views.approveBlog, name = 'approveBlog'),
    path('comment/<id>/', views.comment, name = 'comment'),
    path('singleBlog/<id>/', views.singleBlog, name = 'singleBlog'),
    path('post/<int:pk>/like/', AddLike.as_view(), name = 'like'),
    path('post/<int:pk>/dislike/', AddDislike.as_view(), name = 'dislike'),

    path('block/<int:id>/',views.block, name = 'block'),
    path('delete/<int:id>/',views.delete, name = 'delete'),
    path('postDelete/<int:id>/',views.postDelete, name = 'postDelete'),


]
