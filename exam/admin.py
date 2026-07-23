from django.contrib import admin
from exam.models import Exam, Tag, Quiz, QuizOption

admin.site.register(Exam)
admin.site.register(Tag)
admin.site.register(Quiz)
admin.site.register(QuizOption)