from django.urls import path 
from exam.views import MyExams, CreateNewExam


urlpatterns = [
    path('of-mine', MyExams, name="myexams"),
    path('create-new', CreateNewExam, name="createnewexam"),
]