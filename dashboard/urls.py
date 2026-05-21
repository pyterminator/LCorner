from django.urls import path
from dashboard.views import Dashboard

urlpatterns = [
    path('', Dashboard, name="dashboard"),
]