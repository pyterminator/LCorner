from member.models import Account
from django.dispatch import receiver
from django.contrib.auth.models import User
from notifications.models import Notification
from django.db.models.signals import post_save

@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        new_account = Account.objects.create(user=instance, xp=100)
        notifications = []

        notifications.append(
            Notification(
                account=new_account,
                title = "Təbriklər!!!",
                type="SYSTEM",
                message="⭐ Qeydiyyatdan keçdiyiniz üçün sistem tərəfindən balansınıza +100 xal əlavə edildi."
            )
        )

        super_admins = Account.objects.filter(
            user__is_superuser=True
        ).select_related("user")

        for admin in super_admins:
            notifications.append(
                Notification(
                    title="Yeni istifadəçi",
                    account=admin,
                    actor=new_account,
                    type="SYSTEM",
                    message=f"Yeni istifadəçi qeydiyyatdan keçdi: {instance.username}"
                )
            )

        Notification.objects.bulk_create(notifications)



@receiver(post_save, sender=User)
def save_user_account(sender, instance, **kwargs):
    # Əgər hər hansı səbəbdən account yoxdursa, xəta verməməsi üçün hasattr yoxlanışı

    #// if hasattr(instance, "account"):
    #//    instance.account.save()

    try:
        instance.account.save()
    except Account.DoesNotExist:
        pass


 