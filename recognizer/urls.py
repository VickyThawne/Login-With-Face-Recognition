from django.contrib import admin
from django.urls import path

from .views import (
    home_view,
    login_view,
    signup_view,
    update_profile,
    profile_view,
    logout_view,
)

app_name = 'recognizer'

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('update-profile/<int:pk>', update_profile, name='update-profile'),
    path('profile/<int:pk>', profile_view, name='profile'),
    
]