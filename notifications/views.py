from django.shortcuts import render
from notifications.models import Notification
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required 
def MyNotifications(request):

    my_notifications = Notification.objects.filter(account__user=request.user).all()

    data = {
        "notifications": my_notifications
    }

    return render(request, 'dashboard/notifications.html', context=data)


@login_required
def GetUnreadNotificationCount(request):

    if request.method != "POST": return JsonResponse({"success": False})

    try:
        count_of_unread_notifications = Notification.objects.filter(account__user=request.user).filter(is_read=False).count()

        return JsonResponse({
            "count_of_unread_notifications": count_of_unread_notifications,
            "success": True,
            "has_unread_notifications": count_of_unread_notifications > 0
        })
    except:
        return JsonResponse({"success": False})
    