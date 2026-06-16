from django.urls import path 
from exam.views import MyExams


urlpatterns = [
    path('of-mine', MyExams, name="myexams"),
]