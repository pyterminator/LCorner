from django.urls import path 
from notifications.views import MyNotifications, GetUnreadNotificationCount, CheckAsRead

urlpatterns = [
    path("", MyNotifications, name="mynotifications"),
    path("check-as-read/", CheckAsRead, name="checkasread"),
    path("get-unread-notification-count/", GetUnreadNotificationCount, name="getunreadnotificationcount"),
]