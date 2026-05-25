from django.urls import path 
from member.views import (
    MemberLogin, MemberRegistration, MemberLogout, 
    UserAccount, ChangeMyPassword, ChangeMyAvatar, DeleteMyAvatar,
    AccountList, UpdateBaseData, SaveBioData
)


urlpatterns = [
    path('', MemberLogin, name="login"),
    path('logout', MemberLogout, name="logout"),
    path('register', MemberRegistration, name="register"),
    path('change-my-password',ChangeMyPassword, name="changemypassword"), 
    path('change-my-avatar',ChangeMyAvatar, name="changemyavatar"), 
    path('delete-my-avatar',DeleteMyAvatar, name="deletemyavatar"), 
    path('update-base-data',UpdateBaseData, name="updatebasedata"), 
    path('update-bio-data',SaveBioData, name="updatebiodata"), 
    path('accounts', AccountList, name="accounts"),
    path('@<str:username>', UserAccount, name="myaccount"),
]