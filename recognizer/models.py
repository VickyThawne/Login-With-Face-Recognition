from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save

import os

from .utils import random_string_generator


def user_image_path(instance, filename):
    name, ext = filename.split('.')
    name = instance.user.first_name + instance.unique_id
    filename = name + '.' + ext
    return 'User_images/{}/{}'.format(instance.gender, filename)


def unique_id_generator(instance, new_id=None):
    """
    This is for a Django project and it assumes your instance 
    has a model with a slug field and a title character (char) field.
    """
    if new_id is not None:
        unique_id = new_id
    else:
        unique_id = slugify(instance.user.username)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(unique_id=unique_id).exists()
    if qs_exists:
        new_slug = "{unique_id}-{randstr}".format(
                    unique_id=unique_id,
                    randstr=random_string_generator(size=4)
                )
        return unique_id_generator(instance, new_slug=new_slug)
    return unique_id


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
    
    
    
def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Item)
