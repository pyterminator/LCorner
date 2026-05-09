from django.urls import path
from dashboard.views import Dashboard, Levels, CreateLevel, LevelDetail, QuizModels

urlpatterns = [
    path('', Dashboard, name="dashboard"),
    path('levels/', Levels, name="levels"),
    path('levels/create-new/', CreateLevel, name="createlevel"),
    path('levels/detail/<int:id>/', LevelDetail, name="leveldetail"),

    path('quizmodels/', QuizModels, name='quizmodels'),
]