import logger


class MetaEventHandler:
    """元事件处理器"""

    def __init__(self, websocket, msg):
        self.websocket = websocket
        self.msg = msg
        self.post_type = msg.get("post_type", "")

    async def handle(self):
        logger.info(f"[Example]收到元事件")
