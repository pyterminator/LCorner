from django.urls import path 
from exam.views import MyExams, CreateNewExam, SentenceBuilder, UpdateExam, ActivateExam, ExamDetailView


urlpatterns = [
    path('of-mine', MyExams, name="myexams"),
    path('create-new', CreateNewExam, name="createnewexam"),
    path('update/<str:slug>', UpdateExam, name="updateexam"),
    path('exam-detail/<str:slug>', ExamDetailView, name="examdetail"),
    path('activate-exam/<int:id>', ActivateExam, name="activateexam"),
    path("system-sentence-builder-game", SentenceBuilder, name="sentencebuilder"),
]