from django.urls import path 
from exam.views import MyExams, CreateNewExam, SentenceBuilder


urlpatterns = [
    path('of-mine', MyExams, name="myexams"),
    path('create-new', CreateNewExam, name="createnewexam"),
    path("system-sentence-builder-game", SentenceBuilder, name="sentencebuilder"),
]