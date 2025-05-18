class MessageHandler:
    """消息处理器"""

    def __init__(self, websocket, msg):
        self.websocket = websocket
        self.msg = msg
        self.time = msg.get("time", "")
        self.message_type = msg.get("message_type", "")

    async def handle_group(self):
        """
        处理群消息
        """
        pass

    async def handle_private(self):
        """
        处理私聊消息
        """
        pass

    async def handle(self):
        if self.message_type == "group":
            await self.handle_group()
        elif self.message_type == "private":
            await self.handle_private()
