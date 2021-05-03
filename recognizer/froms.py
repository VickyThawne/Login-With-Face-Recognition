from django import forms

from .models import User, UserProfile

class AuthenticationForm(froms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta():
        model = User
        fields = ['username', 'email', 'password']
        
        
class UserProfileForm(forms.ModelForm):
    class Meta():
        model = UserProfile
        exclude = ['unique_id']