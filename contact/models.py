from django.db import models

class Message(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    message = models.CharField(max_length=255)

    is_public = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)