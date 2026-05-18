from django.conf import settings
from django.contrib import admin
from django.urls import path, include 
from django.conf.urls.static import static

urlpatterns = [
    path('', include("member.urls")),
    path('contact/', include("contact.urls")),
    path('dashboard/', include("dashboard.urls")),
    path('post/', include("post.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
