from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def send_user_update(user):
    from notifications.models import Notification

    account = user.account

    unread_count = Notification.objects.filter(
        account=account,
        is_read=False
    ).count()

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        f"user_{user.id}",
        {
            "type": "notification_update",
            "xp": account.xp,
            "level": account.level,
            "notification_count": unread_count,
        },
    )