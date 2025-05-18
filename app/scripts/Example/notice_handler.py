import logger


class NoticeHandler:
    """通知处理器"""

    def __init__(self, websocket, msg):
        self.websocket = websocket
        self.msg = msg

    async def handle(self):
        logger.info(f"[Example]收到通知")
