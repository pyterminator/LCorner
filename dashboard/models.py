from django.db import models
from member.models import Account
from post.models import Post

class Like(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE,  related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes_set")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('account', 'post')