from django import forms
from django.contrib.auth.forms import UserCreationForm

from login_details.models import LoginDetails

from .models import User, UserProfile

class AuthenticationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    
        
    
    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        
        
        
class UserProfileForm(forms.ModelForm):
    birth_date = forms.DateField(widget = forms.SelectDateWidget())
    class Meta():
        model = UserProfile
        fields = ['image', 'about', 'gender', 'birth_date',
                  'phone_number', 'website', 'github_username',
                  'twitter_handle', 'instagram_username', 'facebook_username', "college", "company", "branch"]

        
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            
class LectureDetailsForm(forms.ModelForm):
    class Meta():
        model = LoginDetails
        fields = ['teacher', 'lecture']
    
    # def __init__(self, *args, **kwargs):
    #     super(LectureDetailsForm, self).__init__(*args, **kwargs)
    #     for visible in self.visible_fields():
    #         visible.field.widget.attrs['class'] = 'form-control'
            
            
    