from django.urls import path 
from exam.views import (
    MyExams, CreateNewExam, SentenceBuilder, UpdateExam, ActivateExam, 
    ExamDetailView, ExamPano, GenerateQuizForExamPano, CheckAnswer, 
    CheckIsFullExamWithQuestions, EnrollExam )


urlpatterns = [
    path('of-mine', MyExams, name="myexams"),
    path('enroll-exam', EnrollExam, name="enrollexam"),
    path('create-new', CreateNewExam, name="createnewexam"),
    path('update/<str:slug>', UpdateExam, name="updateexam"),
    path('exam-detail/<str:slug>', ExamDetailView, name="examdetail"),
    path('exam-pano/checkanswer', CheckAnswer, name='exampanocheckanswer'),
    path('exam-pano/<str:slug>', ExamPano, name="exampano"),
    path('generate-quiz-for-exam-pano/<str:slug>', GenerateQuizForExamPano, name="generatequizforexampano"),
    path('activate-exam/<int:id>', ActivateExam, name="activateexam"),
    path("system-sentence-builder-game", SentenceBuilder, name="sentencebuilder"),
    path('check-exam-question-count', CheckIsFullExamWithQuestions, name="checkisfullexamwithquestions"),
]