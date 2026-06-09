from django.urls import path 
from member.views import (
    MemberLogin, MemberRegistration, MemberLogout, 
    UserAccount, ChangeMyPassword, ChangeMyAvatar, DeleteMyAvatar,
    AccountList, UpdateBaseData, SaveBioData, ChangeUsername, ChangeUserStaff,
    GetPostsAjax
)


urlpatterns = [
    path('', MemberLogin, name="login"),
    path('logout', MemberLogout, name="logout"),
    path('register', MemberRegistration, name="register"),
    path('change-my-password',ChangeMyPassword, name="changemypassword"), 
    path('change-my-username',ChangeUsername, name="changemyusername"), 
    path('change-my-avatar',ChangeMyAvatar, name="changemyavatar"), 
    path('update-base-data',UpdateBaseData, name="updatebasedata"), 
    path('update-bio-data',SaveBioData, name="updatebiodata"), 
    path('accounts', AccountList, name="accounts"),
    path('@<str:username>', UserAccount, name="myaccount"),
    path('change-user-staff', ChangeUserStaff, name="changeuserstaff"),
    path('get-posts-ax', GetPostsAjax, name="getpostsajax"),
]