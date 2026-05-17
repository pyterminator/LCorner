from django.urls import path 
from post.views import post_create_view

urlpatterns = [
    path('create/', post_create_view, name="postcreate"),
]