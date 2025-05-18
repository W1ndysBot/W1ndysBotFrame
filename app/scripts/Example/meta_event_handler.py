import logger


class MetaEventHandler:
    """元事件处理器"""

    def __init__(self, websocket, msg):
        self.websocket = websocket
        self.msg = msg

    async def handle(self, msg):
        logger.info(f"[Example]收到元事件")
        pass
