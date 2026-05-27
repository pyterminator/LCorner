from django.db import models
from member.models import Account


class Notification(models.Model):
    TYPE_CHOICES = (
        ('LEVEL_UP', 'Level Up'),
        ('NEW_POST', 'New Post'),
        ('LIKE', 'Like'),
        ('COMMENT', 'Comment'), 
        ('SYSTEM', 'System'),
    )

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="notifications")
    actor = models.ForeignKey(Account, null=True, blank=True, on_delete=models.SET_NULL, related_name="notification_actions")

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=100)
    message = models.CharField(max_length=255)

    data = models.JSONField(null=True, blank=True)
    url = models.CharField(max_length=255, blank=True)

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.account.user.username} - {self.type}"
