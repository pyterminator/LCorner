from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Level(models.Model):
    name = models.CharField(max_length=250)
    q_count = models.IntegerField(
        validators=[
            MinValueValidator(5), MaxValueValidator(50)
        ]
    )
    scorepq = models.IntegerField()
    ispaid = models.BooleanField(default=False)
    price = models.IntegerField(
        validators=[
            MinValueValidator(0), MaxValueValidator(50)
        ]
    )

    is_public = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ContactMessage(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    message = models.CharField(max_length=255)

    is_public = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
