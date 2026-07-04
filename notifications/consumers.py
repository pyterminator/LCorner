from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

class NotificationConsumer(WebsocketConsumer):

    def connect(self):

        if self.scope["user"].is_anonymous:
            self.close()
            return

        self.group_name = f"user_{self.scope['user'].id}"

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):

        if hasattr(self, "group_name"):
            async_to_sync(self.channel_layer.group_discard)(
                self.group_name,
                self.channel_name
            )


    def notification_update(self, event):

        self.send(text_data=json.dumps({
            "xp": event["xp"],
            "level": event["level"],
            "notification_count": event["notification_count"]
        }))