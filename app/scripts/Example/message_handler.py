import logger


class MessageHandler:
    """消息处理器"""

    def __init__(self, websocket, msg):
        self.websocket = websocket
        self.msg = msg
        self.message_type = msg.get("message_type", "")

    async def handle(self):

        logger.info(f"[Example]收到消息")
