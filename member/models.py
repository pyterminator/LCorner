import random 
import string
from django.db import models
from django.contrib.auth.models import User 


def get_random_avatar_name(instance, filename):
    # Şəklin uzantısını götürürük (məsələn: '.jpg', '.png')
    ext = filename.split(".")[-1]

    # 10 simvollu random string yaradırıq (hərflər və rəqəmlərdən ibarət)
    random_str = "".join(
        random.choices(string.ascii_letters + string.digits, k=10)
    )

    # Yeni adı formalaşdırırıq: "avatars/abc123xyz8.jpg"
    return f"avatars/{random_str}.{ext}"


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(upload_to=get_random_avatar_name, blank=True, null=True)
    
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
