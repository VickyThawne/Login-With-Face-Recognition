from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404, reverse, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http.response import StreamingHttpResponse
from django.views.decorators import gzip

import cv2

from .models import UserProfile, User
from .forms import UserProfileForm, AuthenticationForm
from .recognizer import recognizer, Recognizer, RecognizerClass

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
    context['login_object'] = login_instance
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

def gen(camera):
    while True:
        (names, known_face_names, proceed_login, jpeg) = camera.get_frame()
        frame = jpeg
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')




@login_required(login_url = 'recognizer:login')
def login_with_face(request):
    context = {}
    jpeg = None
    details = None
    user = None
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
        
        names, known_lables, login_proceed, jpeg = Recognizer(details, username=user.user.username, unique_id=user.unique_id)
        
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
        
    





@login_required(login_url = 'recognizer:login')
@gzip.gzip_page
def login_with_face_part2(request):
    details = {}
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
        

    
    return StreamingHttpResponse(gen(RecognizerClass(details, username=user.user.username, unique_id=user.unique_id, request=request)),
    			content_type='multipart/x-mixed-replace; boundary=frame')
        
        
        
        
  
# import cv2
# import face_recognition
# import os
# import numpy as np      
        

# def gen_part2(camera):
#     while True:
#         frame = camera
#         yield (b'--frame\r\n'
#                 b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        

# def login_with_face_part3(request):
    
#     try:
#         user = UserProfile.objects.get(user=request.user)

#         gender = user.gender
#         details = {
#         'gender':gender,
#         'username':user.user.username,
#         'unique_id':user.unique_id,
#         'user':user,
#         }
#     except:
#         details = None
    
#     video = cv2.VideoCapture(0)

#     known_face_encodings = []
#     known_face_names = []

#     # base_dir = os.path.dirname(os.path.abspath(__file__))
#     # image_dir = os.path.join(base_dir, "static")
#     # image_dir = os.path.join(image_dir, "profile_pics")

#     # base_dir = os.getcwd()
#     base_dir = os.path.dirname(os.path.abspath(__file__))
#     # os.chdir("..")
#     base_dir = os.getcwd()
#     image_dir = os.path.join(base_dir,"{}\{}\{}".format('media','User_images',details['gender']))
#     # print(image_dir)
#     names = []
#     proceed_login = False


#     for root,dirs,files in os.walk(image_dir):
#         for file in files:
#             if file.endswith('jpg') or file.endswith('png'):
#                 path = os.path.join(root, file)
#                 img = face_recognition.load_image_file(path)
#                 label = file[:len(file)-4]
#                 img_encoding = face_recognition.face_encodings(img)[0]
#                 known_face_names.append(label)
#                 known_face_encodings.append(img_encoding)

#     face_locations = []
#     face_encodings = []



#     while True:	

#         check, frame = video.read()
#         try:
#             small_frame = cv2.resize(frame, (0,0), fx=0.5, fy= 0.5, interpolation=cv2.INTER_AREA)
#         except:
#             break
    
#         rgb_small_frame = small_frame[:,:,::-1]

#         face_locations = face_recognition.face_locations(rgb_small_frame)
#         face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
#         face_names = []


#         for face_encoding in face_encodings:

#             matches = face_recognition.compare_faces(known_face_encodings, np.array(face_encoding), tolerance = 0.6)

#             face_distances = face_recognition.face_distance(known_face_encodings,face_encoding)	
            
#             try:
#                 matches = face_recognition.compare_faces(known_face_encodings, np.array(face_encoding), tolerance = 0.6)

#                 face_distances = face_recognition.face_distance(known_face_encodings,face_encoding)
#                 best_match_index = np.argmin(face_distances)

#                 if matches[best_match_index]:
#                     name = known_face_names[best_match_index]
#                     face_names.append(name)
#                     if name not in names:
#                         names.append(name)
#             except:
#                 pass

#         if len(face_names) == 0:
#             for (top,right,bottom,left) in face_locations:
#                 top*=2
#                 right*=2
#                 bottom*=2
#                 left*=2

#                 cv2.rectangle(frame, (left,top),(right,bottom), (0,0,255), 2)

#                 # cv2.rectangle(frame, (left, bottom - 30), (right,bottom - 30), (0,255,0), -1)
#                 font = cv2.FONT_HERSHEY_DUPLEX
#                 cv2.putText(frame, 'Unknown', (left, top), font, 0.8, (255,255,255),1)
#                 proceed_login = False
#         else:
#             for (top,right,bottom,left), name in zip(face_locations, face_names):
#                 top*=2
#                 right*=2
#                 bottom*=2
#                 left*=2

#                 cv2.rectangle(frame, (left,top),(right,bottom), (0,255,0), 2)

#                 # cv2.rectangle(frame, (left, bottom - 30), (right,bottom - 30), (0,255,0), -1)
#                 font = cv2.FONT_HERSHEY_DUPLEX
#                 cv2.putText(frame, name, (left, top), font, 0.8, (255,255,255),1)
#                 if (details['username']+user.unique_id) in name:
#                     proceed_login = True
#                 else:
#                     proceed_login = False

#         # cv2.imshow("Face Recognition Panel",frame)
#         ret, jpeg = cv2.imencode('.jpg', frame)

#         if cv2.waitKey(1) == ord('q'):
#             if str(request.user.username + user.unique_id) in names:
#                 user.login_proceed = proceed_login
                
#                 instance = LoginDetails.objects.create(user=request.user)
#                 instance.save()
#                 user.save()
                
#                 messages.success(request, 'now you canwatch premium content')
#             else:
#                 user.login_proceed = proceed_login
#                 user.save()
#                 messages.error(request, 'stfu b** get your ass out of my website..')
#             break
            
        
            
#     video.release()
#     cv2.destroyAllWindows()
    
#     print(jpeg.tobytes())
#     return StreamingHttpResponse(gen_part2(jpeg.tobytes()),
#     			content_type='multipart/x-mixed-replace; boundary=frame')
    
    
    
        
    
    
    
from django import template

register = template.Library()

@register.simple_tag
def current_pk(user):
    return UserProfile.objects.get(user=user).pk   