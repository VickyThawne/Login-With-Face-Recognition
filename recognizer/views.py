from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import UserProfile, User
from .forms import UserProfileForm, AuthenticationForm
from .recognizer import recognizer, Recognizer

from login_details.models import LoginDetails

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
    try:
        user = request.user
        user = UserProfile.objects.get(user=user)
        context['user'] = user
        context['premium_data'] = LoginDetails.objects.filter(user=request.user)
    except:
        return redirect('recognizer:login')
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
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user=user)
                messages.success(request, 'login sucsessful!')
                uqid = get_uqid(request)
                request.session['uqid'] = uqid
                
                request.session['user_pk'] = UserProfile.objects.get(user=user).pk
                
                login_form = AuthenticationForm(request.POST or None)
                context['form'] = login_form
                
                user_profile = UserProfile.objects.get(user=user)
                if user_profile.image:
                    return redirect('recognizer:home')
                else:
                    return redirect(reverse('recognizer:update-profile', kwargs={'pk': user.pk}))
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
            
            user = authenticate(request, username=username, password=password)
            if user is None:
                user = User.objects.create(username=username, email=email, password=password)
                # user.set_password(password)
                user.save()
                login(request, user=user)
                
                signup_form = AuthenticationForm(request.POST or None)
                context['form'] = signup_form
                messages.success(request, "Sign up Sucsessful")
                
                # uqid = get_uqid(request=request)
                # request.session['uqid'] = uqid
                return redirect('recognizer:home')
            else:
                messages.error(request, 'User already exists!')
                context['form'] = signup_form
                return render(request, 'recognizer/signup.html', context=context)
                
    return render(request, 'recognizer/signup.html', context=context)


@login_required(login_url='recognizer:login')
def profile_view(request, pk=None):
    instance = get_object_or_404(UserProfile, pk=pk)
    login_instance = get_list_or_404(LoginDetails, user=request.user)
    context = {}
    if request.user == instance.user or request.user.is_staff:
        context['object'] = instance
        context['login_object'] = login_instance
    return render(request, 'recognizer/profile.html', context=context)


@login_required(login_url='recognizer:login')
def update_profile_view(request, pk=None):
    instance = get_object_or_404(UserProfile, pk=pk)
    edit_form = UserProfileForm(request.POST or None, instance=instance)
    if instance.user == request.user or request.user.is_superuser:
        context = {
            'form':edit_form,
        }
        if request.POST:
            if edit_form.is_valid():
                
                first_name = edit_form.cleaned_data.get('first_name')
                user_instance = User.objects.get(pk=request.user.pk)
                user_instance.first_name = first_name
                user_instance.save()
                
                user = edit_form.save()
                messages.success(request, "Profile Edited Sucsessfuly")
                request.session['uqid'] = user.unique_id
                return reverse("recognizer:profile", kwargs={'pk': pk})
            else:
                context = {
                    'form':edit_form,
                }
                messages.error(request, "Somthing is wrong , i can feel it")
    else:
        messages.error(request, "Somthing is wrong , i can feel it part 2")
    return render(request, 'recognizer/profile_form.html', context=context)



@login_required(login_url='recognizer:login')
def logout_confirm_view(request):
    context = {}
    context['view'] = 'Logout'
    context['msg'] = 'Wanna Logout??'
    return render(request, 'recognizer/anything-confirm.html', context=context)


@login_required(login_url='recognizer:login')
def logout_view(request):
    user = UserProfile.objects.get(user=request.user)
    user.login_proceed = False
    user.save()
    logout(request)
    messages.success(request, "Logout Sucsessful")
    return redirect('recognizer:home')



def get_uqid(request):
    user = UserProfile.objects.get(user=request.user)
    return user.unique_id


@login_required(login_url = 'recognizer:login')
def login_with_face(request):
    context = {}
    if request.method == 'POST':
        try:
            user = UserProfile.objects.get(user=request.user)

            gender = user.gender
            details = {
            'gender':gender,
            'username':user.user.username,
            'unique_id':user.unique_id,
            'user':user,
            }
        except:
            details = None
        
        names, known_lables, login_proceed = Recognizer(details, username=user.user.username, unique_id=user.unique_id)
        
        print(names, known_lables, login_proceed)
        
        if str(request.user.username + user.unique_id) in names:
            context['login_detail'] = True
            user.login_proceed = login_proceed
            
            instance = LoginDetails.objects.create(user=request.user)
            instance.save()
            user.save()
            
            messages.success(request, 'now you canwatch premium content')
            return redirect('recognizer:home')
        else:
            context['login_detail'] = False
            user.login_proceed = login_proceed
            user.save()
            messages.error(request, 'stfu b** get your ass out of my website..')
            return redirect('recognizer:home')
        
        
    return render(request, 'recognizer/home.html', context=context)
        
        
        
        
from django import template

register = template.Library()

@register.simple_tag
def current_pk(user):
    return UserProfile.objects.get(user=user).pk   