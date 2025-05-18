from .group_message_handler import GroupMessageHandler
from .private_message_handler import PrivateMessageHandler


class MessageHandler:
    """消息处理器"""

    def __init__(self, websocket, msg):
        self.websocket = websocket
        self.msg = msg
        self.message_type = msg.get("message_type", "")

    async def handle(self):
        if self.message_type == "group":
            await GroupMessageHandler(self.websocket, self.msg).handle()
        elif self.message_type == "private":
            await PrivateMessageHandler(self.websocket, self.msg).handle()
