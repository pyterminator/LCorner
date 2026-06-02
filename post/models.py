import uuid
from django.db import models
from member.models import Account
from django.utils.text import slugify

class Post(models.Model):

    LANG_CHOICES  = (
        ("EN", "EN"),
        ("RU", "RU"),
        ("GE", "GE"),
    )

    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    lang = models.CharField(choices=LANG_CHOICES , default=LANG_CHOICES [0][0], max_length=10)
    sentence = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(unique=True, blank=True, max_length=100)
    likes = models.PositiveIntegerField(default=0)
    view = models.PositiveBigIntegerField(default=0)

    is_public = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.sentence)[:50]
            self.slug = f"{base}-{uuid.uuid4().hex[:6]}"
        super().save(*args, **kwargs)