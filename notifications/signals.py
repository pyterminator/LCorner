from member.models import Account
from django.dispatch import receiver  
from notifications.models import Notification
from django.db.models.signals import post_save, pre_save

@receiver(pre_save, sender=Account)
def store_old_level(sender, instance, **kwargs):
    if instance.pk:
        instance._old_level = Account.objects.get(pk=instance.pk).level
    else:
        instance._old_level = instance.level

@receiver(post_save, sender=Account)
def level_up_notification(sender, instance, created, **kwargs):
    if created: return

    old_level = getattr(instance, "_old_level", instance.level)

    if instance.level > old_level:
        Notification.objects.create(
            account=instance,
            type="LEVEL_UP",
            message=f"🎉 Təbrik edirəm, sənin saytdakı yeni levelin : {instance.level}"
        )