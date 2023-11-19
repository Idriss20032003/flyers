from django import template
import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from django.utils.timesince import timesince
from .models import Message, Room
register = template.Library()


@register.filter(sender='initials')
def initials(value):
    initials = ''

    for name in value.split(''):
        if name and len(initials) < 3:
            initials += name[0].upper()

    return initials


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.eId = self.scope['url_route']['kwargs']['room_name']
        self.group_event_id = f'chat_{self.eId}'
        user = self.scope['user']
        user_id = user.id if user.is_authenticated else None

        await self.get_room()
        await self.channel_layer.group_add(self.group_event_id, self.channel_name)
        await self.send(text_data=json.dumps({'user_id': user_id}))
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_event_id, self.channel_name)

    async def receive(self, text_data):
        # receive message from websocket
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        message = text_data_json['message']
        name = text_data_json['name']
        sender_id = text_data_json['sender_id']

        print('Receive', type)
# PAS OUBLIER D'ENVOYER DEPUIS LE FRONTEND L'ID DE L'UTILISATEUR CONNECTE !
# typiquement : { "content": "Contenu du message","sender_id": 123 // Identifiant de l'utilisateur
        if type == 'message':
            new_message = self.create_message(name, message)
            await self.channel_layer.group_send(
                self.group_event_id, {
                    'type': 'chat_message',
                    'message': message,
                    'name': name,
                    'sender_id': sender_id,
                    'initials': initials(name),
                    'created_at': timesince(new_message.created_at)}
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'message': event['message'],
            'name': event['name'],
            'sender_id': event['sender_id'],
            'initials': event['initials'],
            'created_at': event['created_at']
        }))

    @sync_to_async
    def get_room(self):
        self.room = Room.objects.get(eId=self.eId)

    @sync_to_async
    def create_message(self, sent_by, message):
        message = Message.objects.create(body=message, sent_by=sent_by)
        message.save()
        self.room.messages.add(message)

        return message

# name -> nom du sender /
#!!!!LORS DE L'ENVOI DE MESSAGES : récupérer le nom du groupe !
