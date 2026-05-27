from member.models import Account
from django.dispatch import receiver
from django.contrib.auth.models import User
from notifications.models import Notification
from django.db.models.signals import post_save

@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        new_account = Account.objects.create(user=instance, xp=100)
        Notification.objects.create(
            account=new_account,
            type="SYSTEM",
            message=f"⭐ Qeydiyyatdan keçdiyiniz üçün sistem tərəfindən balansınıza +100 xal əlavə edildi."
        )



@receiver(post_save, sender=User)
def save_user_account(sender, instance, **kwargs):
    # Əgər hər hansı səbəbdən account yoxdursa, xəta verməməsi üçün hasattr yoxlanışı
    if hasattr(instance, "account"):
        instance.account.save()