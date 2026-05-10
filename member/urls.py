from django.urls import path 
from member.views import MemberLogin, MemberRegistration, MemberLogout

urlpatterns = [
    path('', MemberLogin, name="login"),
    path('logout', MemberLogout, name="logout"),
    path('register', MemberRegistration, name="register"),
]