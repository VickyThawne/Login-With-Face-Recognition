from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404, reverse, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http.response import HttpResponse, StreamingHttpResponse
from django.views.decorators import gzip

import cv2

from .models import TeacherProfileModel, UserProfile, User
from .forms import UserProfileForm, AuthenticationForm, LectureDetailsForm
from .recognizer import recognizer, Recognizer, frame_check

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
    context['data'] = 'Add your cool photo to your profile !'
    login_details_form = LectureDetailsForm(request.POST or None)
    context['login_details_form'] = login_details_form
    teacher=False
    try:
        user = request.user
        try:
            user = TeacherProfileModel.objects.get(user=user)
            teacher = True
        except:
            user = UserProfile.objects.get(user=user)
        
        context['user'] = user
        context['teacher'] = teacher
        context['premium_data'] = LoginDetails.objects.filter(user=request.user)
    except:
        return redirect('recognizer:login')
    
    # this is new 
    if request.method == 'POST' and login_details_form.is_valid():

        try:
            user = UserProfile.objects.get(user=request.user)
             
            gender = user.gender
            details = {
            'gender':gender,
            'username':user.user.username,
            'unique_id':user.unique_id,
            'user':user,
            }
            print(details)
        except:
            details = None
        
        names, known_lables, login_proceed = Recognizer(details, username=user.user.username, unique_id=user.unique_id)
        
        print(names, known_lables, login_proceed)
        print(request.user.username + user.unique_id)

        if str(request.user.username + user.unique_id) in names:
            context['login_detail'] = True
            user.login_proceed = login_proceed
            instance = LoginDetails.objects.create(user=request.user, lecture=login_details_form.cleaned_data.get('lecture'), teacher=login_details_form.cleaned_data.get('teacher'))
            # instance.user=request.user
            instance.save()
            user.save()
            
            context['login_details_form'] = login_details_form
            
            messages.success(request, 'now you canwatch premium content')
            return redirect('recognizer:home')
        else:
            context['login_detail'] = False
            user.login_proceed = login_proceed
            user.save()
            
            context['login_details_form'] = login_details_form
            
            messages.error(request, 'stfu b** get your ass out of my website..')
            return redirect('recognizer:home')
    
    
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
                if user.teacher_profile:
                    if user_profile.image:
                        return redirect('recognizer:home')
                    else:
                        return redirect(reverse('recognizer:update-profile', kwargs={'pk': user_profile.pk}))
                    
                if user_profile.image:
                    return redirect('recognizer:home')
                else:
                    return redirect(reverse('recognizer:update-profile', kwargs={'pk': user_profile.pk}))
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
                
                user_profile = user.user_profile
                # uqid = get_uqid(request=request)
                # request.session['uqid'] = uqid
                return redirect(reverse('recognizer:update-profile', kwargs={'pk': user_profile.pk}))
            else:
                messages.error(request, 'User already exists!')
                context['form'] = signup_form
                return render(request, 'recognizer/signup.html', context=context)
                
    return render(request, 'recognizer/signup.html', context=context)


@login_required(login_url='recognizer:login')
def profile_view(request, pk=None):
    instance = None
    login_instance = None
    try:
        instance = UserProfile.objects.get(pk=pk)
    except:
        pass
    
    try:
        login_instance = LoginDetails.objects.filter(user=request.user)
    except: 
        pass
    
    context = {}
    # if request.user == instance.user or request.user.is_staff:
    context['object'] = instance
    print(instance)
    context['login_object'] = login_instance
    try:
        context['teacher'] = User.objects.get(pk=pk).teacher_profile
    except:
        pass
    return render(request, 'recognizer/profile.html', context=context)


@login_required(login_url='recognizer:login')
def update_profile_view(request, pk=None):
    try: 
        instance = UserProfile.objects.get(pk=pk)
    except:
        instance = None
    edit_form = UserProfileForm(request.POST or None, instance=instance)
    context = {
            'form':edit_form,
        }
    if instance.user == request.user or request.user.is_superuser:
        if request.POST:
            if edit_form.is_valid:
                img = request.FILES.get('image')
                user = edit_form.save()
                instance.image = img
                instance.save()
                
                messages.success(request, "Profile Edited Sucsessfuly")
                request.session['uqid'] = user.unique_id
                context = {
                    'form':edit_form,
                }
                return HttpResponseRedirect(reverse("recognizer:profile", kwargs={'pk': pk}))
            else:
                context = {
                    'form':edit_form,
                }
                messages.error(request, "Somthing is wrong , i can feel it")

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



################################################3
#################################################
####################################################33
#################################################333
###################################################3



@login_required(login_url = 'recognizer:login')
def login_with_face(request):
    

    context = {}

    if request.method == 'POST':
        print("teacher:"+str(request.POST.get('teacher')))
        print("lec:"+str(request.POST.get('lecture')))
        try:
            user = UserProfile.objects.get(user=request.user)
             
            gender = user.gender
            details = {
            'gender':gender,
            'username':user.user.username,
            'unique_id':user.unique_id,
            'user':user,
            }
            print(details)
        except:
            details = None
        
        names, known_lables, login_proceed = Recognizer(details, username=user.user.username, unique_id=user.unique_id)
        
        print(names, known_lables, login_proceed)
        print(request.user.username + user.unique_id)

        if str(request.user.username + user.unique_id) in names:
            context['login_detail'] = True
            user.login_proceed = login_proceed
            instance = LoginDetails.objects.create(user=request.user )
            instance.user=request.user
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
    print(context)
    return render(request, 'recognizer/home.html', context)
        
# from streamer import Streamer



# def gen():
#     streamer = Streamer('localhost', 8080)
#     streamer.start()

#     while True:
#         if streamer.streaming:
#             yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + streamer.get_jpeg() + b'\r\n\r\n')

# @app.route('/')
# def index():
#   return render_template('index.html')

# @app.route('/video_feed')
# def video_feed():
#   return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

        
 
        
        

    
    
from django import template

register = template.Library()

@register.simple_tag
def current_pk(user):
    return UserProfile.objects.get(user=user).pk   