from django.urls import path
from dashboard.views import Dashboard, PostLike

urlpatterns = [
    path('', Dashboard, name="dashboard"),
    path('post-like/', PostLike, name='postlike'),
]