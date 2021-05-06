from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import UserProfile, User
from .forms import UserProfileForm, AuthenticationForm

from django.contrib.auth import (
    login,
    authenticate,
    get_user_model,
    logout
)


# Create your views here.
def home_view(request):
    context = {}
    context['data'] = 'some data'
    return render(request, 'recognizer/home.html', context={})


def login_view(request):
    login_form = AuthenticationForm(request.POST or None)
    context = {}
    context['form'] = login_form
    if request.POST:
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            email = login_form.cleaned_data.get('email')
            password= login_form.cleaned_data.get('password')
            
            user = authenticate(request, username=username, email=email, password=password)
            
            if user is not None:
                login(request, user=user)
                login_form = AuthenticationForm(request.POST or None)
                context['form'] = login_form
                return redirect('recognizer:home')
            else:
                messages.error(request, 'User not found signup first!')
                return render(request, 'recognizer/login.html', context=context)
            
    context = {}
    return render(request, 'recognizer/login.html', context=context)


def signup_view(request):
    signup_form = AuthenticationForm(request.POST or None)
    context = {
        
    }
    context['form'] = signup_form
    
    if request.POST:
        if signup_form.is_valid():
            username = signup_form.cleaned_data.get('username')
            email = signup_form.cleaned_data.get('email')
            password = signup_form.cleaned_data.get('password')
            
            user = authenticate(request, username=username, email=email, password=password)
            if user is None:
                user = User.objects.create(username=username, email=email)
                user.set_password(password)
                user.save()
                signup_form = AuthenticationForm(request.POST or None)
                context['form'] = signup_form
                messages.success(request, "Sign up Sucsessful")
                return redirect('recognizer:home')
            else:
                messages.error(request, 'User already exists!')
                context['form'] = signup_form
                return render(request, 'recognizer/signup.html', context=context)
                

                
    return HttpResponse('sign up')


def update_profile(request, pk=None):
    return HttpResponse('update_profile')


def profile_view(request, pk=None):
    return HttpResponse('profile')


def logout_view(request):
    return HttpResponse('logout')



@login_required(login_url = 'login')
def login_with_face(request):
    if request.method == 'POST':
        details = {
            'branch':request.user.user_profile['gender'],
            }