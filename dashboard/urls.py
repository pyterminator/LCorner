from django.urls import path
from dashboard.views import (
    Dashboard, Levels, CreateLevel, LevelDetail, 
    QuizModels, Users, UserDetail, CreateUser, DeleteUser
)

urlpatterns = [
    path('', Dashboard, name="dashboard"),
    path('levels/', Levels, name="levels"),
    path('levels/create-new/', CreateLevel, name="createlevel"),
    path('levels/detail/<int:id>/', LevelDetail, name="leveldetail"),

    path('quizmodels/', QuizModels, name='quizmodels'),

    path('users/', Users, name="users"),
    path('users/detail/<int:id>', UserDetail, name="userdetail"),
    path('users/create-new/', CreateUser, name="createuser"),
    path('users/delete/<int:id>', DeleteUser, name="deleteuser"),
]