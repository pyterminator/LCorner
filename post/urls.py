from django.urls import path 
from post.views import post_create_view, posts_view, post_approved_view

urlpatterns = [
    path('create/', post_create_view, name="postcreate"),
    path('list/', posts_view, name="posts_admin"),
    path('change-approved/<int:id>', post_approved_view, name="changepostapproved"),
]