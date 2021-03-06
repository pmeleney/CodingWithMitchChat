from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
from django.contrib.auth import get_user_model
from .models import Game

User = get_user_model()

# Example taken from:
# https://github.com/andrewgodwin/channels-examples/blob/master/multichat/chat/consumers.py
class PublicChatConsumer(AsyncJsonWebsocketConsumer):

	async def connect(self):
		"""
		Called when the websocket is handshaking as part of initial connection.
		"""
		print("PublicChatConsumer: connect: " + str(self.scope["user"]))
		# let everyone connect. But limit read/write to authenticated users
		await self.accept()

		# Add them to the group so they get room Messages

		await self.channel_layer.group_add(
			str(self.scope['url_route']['kwargs']['slug']),
			self.channel_name
		)


	async def disconnect(self, code):
		"""
		Called when the WebSocket closes for any reason.
		"""
		# leave the room
		print("PublicChatConsumer: disconnect")
		pass


	async def receive_json(self, content):
		"""
		Called when we get a text frame. Channels will JSON-decode the payload
		for us and pass it as the first argument.
		"""
		# Messages will have a "command" key we can switch on
		command = content.get("command", None)
		print("PublicChatConsumer: receive_json: " + str(command) + "from" + str(self.scope["user"]))
		if command == 'send':
			await self.send_message(content)
		if command == 'drawNew':
			await self.send_message(content)

	async def chat_message(self, event):
		"""
		send a message down to client.
		"""
		print('event', event)
		print("PublicChatConsumer: chat_message_from_user:" + str(event['payload']['username'] + str(event['payload'])))
		await self.send_json({

			"payload": event['payload']

		})

	async def send_message(self, payload):
		await self.channel_layer.group_send(
			str(self.scope['url_route']['kwargs']['slug']),
			{
				"type": "chat.message",
				"payload": payload,
			}
		)
