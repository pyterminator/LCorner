from django.db import models
from django.contrib.auth.models import User 


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    bio = models.CharField(max_length=255, blank=True, null=True)

    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    post_count = models.PositiveIntegerField(default=0)

    linkedin = models.CharField(max_length=255, blank=True, null=True)
    instagram = models.CharField(max_length=255, blank=True, null=True)
    youtube = models.CharField(max_length=255, blank=True, null=True)
    facebook = models.CharField(max_length=255, blank=True, null=True)
    tiktok = models.CharField(max_length=255, blank=True, null=True)
    x = models.CharField(max_length=255, blank=True, null=True)
