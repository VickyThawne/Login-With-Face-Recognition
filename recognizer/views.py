from django.shortcuts import render, HttpResponse, redirect

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