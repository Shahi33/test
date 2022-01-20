from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.models import User
from .forms import UserRegistration
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
# Create your views here.


# register views
def register(request):
    register_form = UserRegistration()
    if request.method == 'POST':
        register_form = UserRegistration(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data.get("username")
            first_name = register_form.cleaned_data.get("first_name")
            last_name = register_form.cleaned_data.get("last_name")
            email = register_form.cleaned_data.get("username")
            password = register_form.cleaned_data.get("password1")
            
            
            new_user = User.objects.create_user(username, email, password, first_name=first_name,last_name=last_name)

            return redirect('users:login')
    context = {'register_form':register_form,}
    return render(request,"users/register.html",context)

# Login views
class MyLoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'


    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        if user.is_superuser:
            success_url = 'admin/'
        else:
            success_url = '/'
        return context  


def myLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('post:adminHome')
            else:
                return redirect('post:home')
            
        else: 
            return HttpResponse("Incorrect Details")
    return render(request,"users/login.html")

class MyLogoutView(SuccessMessageMixin, LogoutView):
    template_name = 'users/login.html'
    success_url = 'users/login'


