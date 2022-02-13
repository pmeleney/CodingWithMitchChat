from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
from django.contrib.auth import get_user_model

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
			"public_chatroom_1",
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
		print("PublicChatConsumer: receive_json: " + str(command))
		if command == 'send':
			if len(content['message'].lstrip()) == 0:
				raise Exception("you can't send an empty message.")
			await self.send_message(content['message'])

	async def send_message(self, message):
		await self.channel_layer.group_send(
			"public_chatroom_1",
			{
				"type": "chat.message",
				"username": self.scope['user'].username,
				"message": message,
			}
		)

	async def chat_message(self, event):
		# send a message to the client.

		print("PublicChatConsumer: chat from user: " + str(event['username']))
		await self.send_json({
			"username": event['username'],
			"message": event['message'],
		})
