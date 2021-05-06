from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required

from .models import UserProfile, User

# Create your views here.
def home_view(request):
    return HttpResponse("hello")


def login_view(request):
    return HttpResponse('login')


def signup_view(request):
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