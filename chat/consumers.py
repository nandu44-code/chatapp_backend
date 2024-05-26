import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.room_name = f"chat_{self.user.id}"
        self.room_group_name = f"chat_{self.room_name}"
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        command = data.get('command', None)

        if command == 'fetch_messages':
            await self.fetch_messages(data['sender'], data['recipient'])
        elif command == 'new_message':
            await self.new_chat_message(data)

    async def fetch_messages(self, sender, recipient):
        messages = await self.get_messages(sender, recipient)
        for message in messages:
            await self.send_message_to_client(message)

    async def new_chat_message(self, data):
        sender = self.user
        recipient_username = data['recipient']
        recipient = await database_sync_to_async(User.objects.get)(username=recipient_username)
        message = data['message']

        new_message = await self.create_message(sender, recipient, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username,
                'recipient': recipient_username
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        recipient = event['recipient']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'recipient': recipient
        }))

    @database_sync_to_async
    def create_message(self, sender, recipient, message):
        return Message.objects.create(sender=sender, recipient=recipient, content=message)

    @database_sync_to_async
    def get_messages(self, sender, recipient):
        sender_user = User.objects.get(username=sender)
        recipient_user = User.objects.get(username=recipient)
        return Message.objects.filter(sender=sender_user, recipient=recipient_user) | Message.objects.filter(sender=recipient_user, recipient=sender_user)

    async def send_message_to_client(self, message):
        await self.send(text_data=json.dumps({
            'message': message.content,
            'sender': message.sender.username,
            'recipient': message.recipient.username,
            'timestamp': str(message.timestamp)
        }))
