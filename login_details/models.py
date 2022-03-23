from django.db import models

from recognizer.models import UserProfile, TeacherProfileModel, LectrueModel
from django.contrib.auth.models import User
import recognizer

# Create your models here.
class LoginDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_date = models.DateField(auto_now_add=True)
    login_time = models.TimeField(auto_now_add=True)
    authenticated_user = models.BooleanField(default=False) 
    teacher = models.ForeignKey("recognizer.TeacherProfileModel", on_delete=models.CASCADE, null=True, blank=True, related_name='login_details_with_teacher')
    lecture = models.ForeignKey(LectrueModel, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        login_date = str(self.login_date)
        login_time = str(self.login_time)
        user = str(self.user)
        return (user +'   '+ login_date +'  Time:  '+ login_time)
    
    class Meta():
        ordering = ['-id']
        verbose_name = 'Login Detail'