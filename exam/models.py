from django.db import models
from member.models import Account


class Exam(models.Model):
    author = models.ForeignKey( Account, on_delete=models.CASCADE, related_name="exams" )
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    duration = models.PositiveIntegerField()
    earn_xp = models.FloatField(default=0)

    rating_total = models.PositiveIntegerField(default=0)
    rating_count = models.PositiveIntegerField(default=0)

    exam_type = models.CharField(
        max_length=20,
        choices=[
            ("limited", "Limited"),
            ("endless", "Endless")
        ]
    )

    difficulty = models.CharField(
        max_length=20,
        choices=[
            ("easy", "Easy"),
            ("medium", "Medium"),
            ("hard", "Hard")
        ]
    )

    price = models.PositiveIntegerField(default=0)


    min_pass_percent = models.PositiveIntegerField(
        default=70
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def rating(self):
        if self.rating_count == 0:
            return 0

        return round(
            self.rating_total / self.rating_count,
            1
        )