
from channels.generic.websocket import WebsocketConsumer
import json

class NotificationConsumer(WebsocketConsumer):

    def connect(self):
        print("WebSocket connected:", self.scope["user"])
        self.accept()

        self.send(text_data=json.dumps({
            "message": "Connected successfully!"
        }))

    def disconnect(self, close_code):
        print("Disconnected")