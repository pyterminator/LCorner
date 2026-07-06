from django.urls import path 
from exam.views import MyExams, CreateNewExam, SentenceBuilder, PublicSentenceBuilder, UpdateExam


urlpatterns = [
    path('of-mine', MyExams, name="myexams"),
    path('create-new', CreateNewExam, name="createnewexam"),
    path('update/<str:slug>', UpdateExam, name="updateexam"),
    path("system-sentence-builder-game", SentenceBuilder, name="sentencebuilder"),
    path("public-sentence-builder-game", PublicSentenceBuilder, name="publicsentencebuilder"),
]