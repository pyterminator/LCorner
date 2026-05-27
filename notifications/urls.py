from django.urls import path 
from notifications.views import MyNotifications, GetUnreadNotificationCount

urlpatterns = [
    path("", MyNotifications, name="mynotifications"),
    path("get-unread-notification-count/", GetUnreadNotificationCount, name="getunreadnotificationcount"),
]