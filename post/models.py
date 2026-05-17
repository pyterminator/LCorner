from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):

    LANG_CHOICES  = (
        ("EN", "EN"),
        ("RU", "RU"),
        ("GE", "GE"),
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    lang = models.CharField(choices=LANG_CHOICES , default=LANG_CHOICES [0][0], max_length=10)
    sentence = models.CharField(max_length=150)
    description = models.CharField(max_length=255)
    likes = models.PositiveIntegerField(default=0)

    is_public = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
