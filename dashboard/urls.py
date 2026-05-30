from django.urls import path
from dashboard.views import Dashboard, CreateDefaultPosts

urlpatterns = [
    path('', Dashboard, name="dashboard"),
    path('create-default-posts/', CreateDefaultPosts, name="createdefaultposts"),
]