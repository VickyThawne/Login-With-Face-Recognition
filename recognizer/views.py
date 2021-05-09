from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
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
    return render(request, 'recognizer/home.html', context=context)


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
                messages.success(request, 'login sucsessful!')
                uqid = get_uqid(request)
                request.session['uqid'] = uqid
                
                login_form = AuthenticationForm(request.POST or None)
                context['form'] = login_form
                
                return redirect('recognizer:home')
            else:
                messages.error(request, 'User not found signup first!')
                return render(request, 'recognizer/login.html', context=context)
            
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
                user = User.objects.create(username=username, email=email, password=password)
                # user.set_password(password)
                user.save()
                
                signup_form = AuthenticationForm(request.POST or None)
                context['form'] = signup_form
                messages.success(request, "Sign up Sucsessful")
                
                uqid = get_uqid(request=request)
                request.session['uqid'] = uqid
                return redirect('recognizer:home')
            else:
                messages.error(request, 'User already exists!')
                context['form'] = signup_form
                return render(request, 'recognizer/signup.html', context=context)
                
    return render(request, 'recognizer/signup.html', context=context)

@login_required(login_url='recognizer:login')
def update_profile(request, pk=None):
    instance = get_object_or_404(UserProfile, pk=pk)
    edit_form = UserProfileForm(request.POST or None, instance=instance)
    context = {
        'form':edit_form,
    }
    if request.POST:
        if edit_form.is_valid():
            user = edit_form.save()
            messages.success(request, "Profile Edited Sucsessfuly")
            request.session['uqid'] = user.unique_id
            return redirect("recognizer:profile", kwargs={ 'pk':pk })
        else:
            context = {
                'form':edit_form,
            }
            messages.error(request, "Somthing is wrong , i can feel it")
    return render(request, 'recognizer/profile-form.html', context=context)


@login_required(login_url='recognizer:login')
def profile_view(request, pk=None):
    instance = get_object_or_404(UserProfile, pk=pk)
    context = {}
    if request.user == instance.user or request.user.is_staff:
        context['object'] = instance
    return render(request, 'recognizer/profile.html', context=context)


@login_required(login_url='recognizer:login')
def logout_confirm_view(request):
    context = {}
    context['view'] = 'Logout'
    context['msg'] = 'Wanna Logout??'
    return render(request, 'recognizer/anything-confirm.html', context=context)


@login_required(login_url='recognizer:login')
def logout_view(request):
    logout(request)
    messages.success(request, "Logout Sucsessful")
    return redirect('recognizer:home')



@login_required(login_url = 'recognizer:login')
def login_with_face(request):
    if request.method == 'POST':
        details = {
            'branch':request.user.user_profile['gender'],
            }
    return HttpResponse('Hey!')


def get_uqid(request):
    user = UserProfile.objects.get(user=request.user)
    return user.unique_id