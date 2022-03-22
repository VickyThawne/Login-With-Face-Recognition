import profile
from django.contrib import admin
from django.urls import path

from .views import profile_view

app_name = 'teacher'


urlpatterns = [
    path('<int:pk>', profile_view, name='dashboard'),
]    
