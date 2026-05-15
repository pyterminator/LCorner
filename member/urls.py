from django.urls import path 
from member.views import MemberLogin, MemberRegistration, MemberLogout, Account, ChangeMyPassword
urlpatterns = [
    path('', MemberLogin, name="login"),
    path('logout', MemberLogout, name="logout"),
    path('register', MemberRegistration, name="register"),
    path('change-my-password',ChangeMyPassword, name="changemypassword"), 
    path('@<str:username>', Account, name="myaccount"),
]