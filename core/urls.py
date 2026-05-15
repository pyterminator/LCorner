from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('', include("member.urls")),
    path('contact', include("contact.urls")),
    path('dashboard', include("dashboard.urls")),
]
