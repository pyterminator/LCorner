from django.urls import path 
from member.views import MemberLogin, MemberRegistration

urlpatterns = [
    path('', MemberLogin, name="login"),
    path('register', MemberRegistration, name="register"),
]