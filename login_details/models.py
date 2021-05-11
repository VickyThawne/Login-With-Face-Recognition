from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class LoginDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_date = models.DateField(auto_now_add=True)
    login_time = models.TimeField(auto_now_add=True)
    authenticated_user = models.BooleanField(default=False)
    
    def __str__(self):
        login_date = str(self.login_date)
        user = str(self.user)
        return (user +' '+ login_date)
    
    class Meta():
        ordering = ['-id']
        verbose_name = 'Login Detail'