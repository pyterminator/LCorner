from django.db import models
from member.models import Account
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

class Exam(models.Model):
    author = models.ForeignKey( Account, on_delete=models.CASCADE, related_name="exams" )
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    duration = models.PositiveIntegerField()
    earn_xp = models.FloatField(default=0)
    question_count = models.PositiveIntegerField(default=0)

    rating_total = models.PositiveIntegerField(default=0)
    rating_count = models.PositiveIntegerField(default=0)

    tags = models.ManyToManyField(
        Tag,
        related_name="exams",
        blank=True
    )

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

    is_active = models.BooleanField(default=False)

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
    

class Quiz(models.Model):
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name="quizzes"
    )

    question = models.TextField()

    order = models.PositiveIntegerField(default=1)

    explanation = models.TextField(
        blank=True,
        default=""
    )

    earn_xp = models.FloatField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question[:50]
    
class QuizOption(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="options"
    )

    text = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to="quiz/options/", blank=True, null=True)
    audio = models.FileField(upload_to="quiz/options/", blank=True, null=True)

    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text