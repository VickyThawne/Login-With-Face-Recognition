from django.db import models
from django.contrib.auth.models import User
import os


def user_image_path(instance, filename):
    name, ext = filename.split('.')
    name = instance.user.first_name + instance.unique_id
    filename = name + '.' + ext
    return 'User_images/{}/{}'.format(instance.gender, filename)


# Create your models here.
class UserProfile(models.Model):
    
    GENDER_CHOICES = (
        ('MALE','M'),
        ('FEMALE','F'),
        ('OTHER', 'O')
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    unique_id = models.CharField(null=True, blank=True, max_length=120)
    image = models.ImageField(upload_to=user_image_path, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=2)
    birth_date = models.DateField(auto_now_add=True, null=True)
    
    def __str__(self):
        return str(self.unique_id+ ' ' + self.user.username)
