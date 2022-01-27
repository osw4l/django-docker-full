import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class UserStatusConsumer(WebsocketConsumer):
    channel_identifier = None

    def connect(self):
        self.channel_identifier = 'orders'
        async_to_sync(self.channel_layer.group_add)(
            self.channel_identifier,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.channel_identifier,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        message = json.loads(text_data)
        async_to_sync(self.channel_layer.group_send)(
            self.channel_identifier,
            {
                'type': 'user_status',
                'message': message
            }
        )

    def user_status(self, notification):
        message = notification['text']
        self.send(text_data=json.dumps(message))

