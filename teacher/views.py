from django.shortcuts import render

from recognizer.models import User, UserProfile, TeacherProfileModel
from login_details.models import LoginDetails

# Create your views here.
def profile_view(request, pk=None):
    context={}
    teacher = TeacherProfileModel.objects.get(user=request.user)
    context['teacher'] = teacher
    return render(request, 'teacher/home/index.html', context=context)