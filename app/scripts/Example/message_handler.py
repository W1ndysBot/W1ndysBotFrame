import logger


class MessageHandler:
    """消息处理器"""

    def __init__(self, websocket, msg):
        self.websocket = websocket
        self.msg = msg

    async def handle(self, msg):
        logger.info(f"[Example]收到消息")
