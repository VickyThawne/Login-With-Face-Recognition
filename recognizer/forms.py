from django import forms
from django.contrib.auth.forms import UserCreationForm

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
    image = forms.ImageField(error_messages={'required': 'Please Upload clear photo of your self!'})
    first_name = forms.CharField()
    class Meta():
        model = UserProfile
        exclude = ['unique_id', 'user', 'login_proceed']

        
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'