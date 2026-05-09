from django.urls import path 
from member.views import MemberLogin

urlpatterns = [
    path('', MemberLogin, name="login"),
]