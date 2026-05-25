import random, string 
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User  
from django.db.models.signals import post_save


def get_random_avatar_name(instance, filename): 
    ext = filename.split(".")[-1] 
    random_str = "".join(
        random.choices(string.ascii_letters + string.digits, k=10)
    ) 
    return f"avatars/{random_str}.{ext}"


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(upload_to=get_random_avatar_name, blank=True, null=True)
    
    bio = models.CharField(max_length=255, blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)

    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    post_count = models.PositiveIntegerField(default=0)

    linkedin = models.CharField(max_length=255, blank=True, null=True)
    instagram = models.CharField(max_length=255, blank=True, null=True)
    youtube = models.CharField(max_length=255, blank=True, null=True)
    facebook = models.CharField(max_length=255, blank=True, null=True)
    tiktok = models.CharField(max_length=255, blank=True, null=True)
    x = models.CharField(max_length=255, blank=True, null=True)




@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:  # Əgər user yeni yaradılıbsa (update edilməyibsə)
        Account.objects.create(user=instance, xp=100)



@receiver(post_save, sender=User)
def save_user_account(sender, instance, **kwargs):
    # Əgər hər hansı səbəbdən account yoxdursa, xəta verməməsi üçün hasattr yoxlanışı
    if hasattr(instance, "account"):
        instance.account.save()