from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save

from login_with_face.settings import BASE_DIR

import os

from .utils import random_string_generator


def user_image_path(instance, filename):
    
    extension = "." + filename.split('.')[-1]
    name = ( instance.user.username + instance.unique_id )
    filename = name + extension 
    
    path = 'User_images/{}/'.format(instance.gender)
    return os.path.join(path , filename)
                    
                    
                    
def unique_id_generator(instance):
    """
    This is for a Django project and it assumes your instance 
    has a model with a slug field and a title character (char) field.
        """
    new_id = random_string_generator(size=12)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(unique_id=new_id).exists()
    if qs_exists:
        new_slug = "{randstr}".format(
                    randstr=random_string_generator(size=12)
                )
        return new_slug
    else:
        return new_id




class UserProfile(models.Model):
    
    GENDER_CHOICES = (
        ('M','MALE'),
        ('F','FEMALE'),
        ('O', 'OTHER')
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_profile')
    unique_id = models.CharField(null=True, blank=True, max_length=120) 
    image = models.ImageField(upload_to=user_image_path, null=True, blank=True)
    about = models.CharField(max_length=30, null=True, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=2, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.IntegerField(default='1234567890')
    website = models.URLField(null=True, blank=True)
    github_username = models.CharField(max_length=100, null=True, blank=True)
    twitter_handle = models.CharField(max_length=100, null=True, blank=True)
    instagram_username = models.CharField(max_length=100, null=True, blank=True)
    facebook_username = models.CharField(max_length=100, null=True, blank=True)
    login_proceed = models.BooleanField(default=False)
    
    
    def __str__(self):
        name = self.user.username + str(self.pk)
        return "{} {}".format(self.user.username, self.pk)
 
    
    
def user_post_save_receiver(sender, instance, *args, **kwargs):
    try:
        obj = UserProfile.objects.get(user=instance)
    except:
        obj = None
    
    if obj is not None:
        pass
    else:
        obj = UserProfile.objects.create(user=instance)
        
    try:    
        if obj.unique_id is None:
            obj.unique_id = unique_id_generator(obj)
            obj.save()
        else:
            pass
    except:
        pass

post_save.connect(user_post_save_receiver, sender=User)
