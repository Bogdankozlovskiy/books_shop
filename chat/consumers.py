from json import loads, dumps
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = loads(text_data)
        message = text_data_json['message']

        self.send(text_data=dumps({
            'message': message
        }))
