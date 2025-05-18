import logger


class ResponseHandler:
    """响应处理器"""

    def __init__(self, websocket, msg):
        self.websocket = websocket
        self.msg = msg

    async def handle(self):
        logger.info(f"[Example]收到响应")
