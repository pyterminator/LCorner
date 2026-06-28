import json
from member.models import Account
from django.http import JsonResponse
from notifications.models import Notification
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

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
            "has_unread_notifications": count_of_unread_notifications > 0,
            "xp":request.user.account.xp,
            "level": request.user.account.level
        })
    except:

        return JsonResponse({"success": False})

@login_required
def CheckAsRead(request):
    if request.method != "POST": return JsonResponse({"success": False})

    try:
        account = get_object_or_404(Account, user=request.user)
        data = json.loads(request.body)
        id = data.get("id", "")
        n = get_object_or_404(Notification, id=id)

        if n and account:
            if n.account == account: 
                if n.is_read:
                    return JsonResponse({"success": False})
                
                n.is_read = True 
                n.save()

                return JsonResponse({
                    "success": n.is_read
                })
        return JsonResponse({"success": False})
    except:
        return JsonResponse({"success": False})
