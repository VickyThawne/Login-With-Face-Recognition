from django.contrib import admin
from django.urls import path

from .views import (
    home_view,
    login_view,
    signup_view,
    update_profile,
    profile_view,
    logout_view,
    logout_confirm_view,
    login_with_face,
)

app_name = 'recognizer'

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('logout-confirm/', logout_confirm_view, name='logout-cnf'),
    path('update-profile/<int:pk>', update_profile, name='update-profile'),
    path('profile/<int:pk>', profile_view, name='profile'),
    path('login-with-face', login_with_face, name='login-with-face')
    
]