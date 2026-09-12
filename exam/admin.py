from django.contrib import admin
from exam.models import Exam, Tag, Quiz, QuizOption, LimitedExamResults

admin.site.register(Exam)
admin.site.register(Tag)
admin.site.register(Quiz)
admin.site.register(QuizOption)
admin.site.register(LimitedExamResults)