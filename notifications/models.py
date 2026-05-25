from django.db import models
from member.models import Account


class Notification(models.Model):
    TYPE_CHOICES = (
        ('LEVEL_UP', 'Level Up'),
        ('NEW_POST', 'New Post'),
        ('LIKE', 'Like'),
        ('COMMENT', 'Comment'),
    )

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="notifications")

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    message = models.CharField(max_length=150)

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account.user.username} - {self.type}"
