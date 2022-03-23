from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from recognizer.models import User, UserProfile, TeacherProfileModel
from login_details.models import LoginDetails
from recognizer.views import login_view

# Create your views here.
@login_required(login_url = 'recognizer:login')
def profile_view(request):
    context={}
    teacher = TeacherProfileModel.objects.get(user=request.user)
    context['teacher'] = teacher
    context['user_profile'] = teacher.user.user_profile.all().first()
    print(teacher.user.user_profile)
    context['students_attended_teachers_lecture'] = LoginDetails.objects.filter(teacher__user__username=request.user.username).order_by('-login_date').order_by('-login_time')
    
    
    return render(request, 'teacher/home/index.html', context=context)