from django.urls import path
from dashboard.views import Dashboard, CreateDefaultPosts, TermsOfUse

urlpatterns = [
    path('', Dashboard, name="dashboard"),
    path('create-default-posts/', CreateDefaultPosts, name="createdefaultposts"),
    path('terms-of-use', TermsOfUse, name='termsofuse'),
]