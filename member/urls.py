from django.urls import path 
from member.views import MemberLogin, MemberRegistration, MemberLogout, UserAccount, ChangeMyPassword, ChangeMyAvatar
urlpatterns = [
    path('', MemberLogin, name="login"),
    path('logout', MemberLogout, name="logout"),
    path('register', MemberRegistration, name="register"),
    path('change-my-password',ChangeMyPassword, name="changemypassword"), 
    path('change-my-avatar',ChangeMyAvatar, name="changemyavatar"), 
    path('@<str:username>', UserAccount, name="myaccount"),
]