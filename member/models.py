import random, string 
from django.db import models
from django.contrib.auth.models import User  
from member.realtime import send_user_update

def generate_unique_code():
    while True:
        code = str(random.randint(10000000, 99999999))
        if not Account.objects.filter(referral_code=code).exists():
            return code


def get_random_avatar_name(instance, filename): 
    ext = filename.split(".")[-1] 
    random_str = "".join(
        random.choices(string.ascii_letters + string.digits, k=10)
    ) 
    return f"avatars/{random_str}.{ext}"


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    referral_code = models.CharField(max_length=8, unique=True, blank=True, null=True)
    referred_by = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="referrals"
    )

    avatar = models.ImageField(upload_to=get_random_avatar_name, blank=True, null=True)
    
    bio = models.CharField(max_length=150, blank=True, null=True)
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


    def required_xp(self, level=None):
        level = level or self.level
        return int(100 + (50 * (level ** 2)))
    
    def xp_percent(self):
        return int((self.xp / self.required_xp()) * 100)

    def add_xp(self, gained_xp): 

        self.xp += gained_xp 

        while self.xp >= self.required_xp(self.level):
            self.level += 1


        self.save()
        send_user_update(self.user)

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = generate_unique_code()
        super().save(*args, **kwargs)




