from concurrent.futures import thread
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import ChatMessage, Thread

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print("connected again")
        user=self.scope['user']
        other_user=self.scope['url_route']['kwargs']['user']
        print(user,other_user)
        thread_obj= self.get_thread(user,other_user)
        self.thread_obj=thread_obj
        print(thread_obj)
        self.chat_room=f"thread_{thread_obj.id}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.chat_room,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user=self.scope['user']
        
        self.create_chat_message(message)
        responseData={'message':message,
        'user':user.username }
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.chat_room,
            {
                'type': 'chat_message',
                'message': responseData
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

    def get_thread(self,user,other_user):
        return  Thread.objects.get_or_new(user,other_user)[0]

    def create_chat_message(self,msg):
        thread_obj=self.thread_obj
        user=self.scope['user']
        return ChatMessage.objects.create(thread=thread_obj,user=user,message=msg)