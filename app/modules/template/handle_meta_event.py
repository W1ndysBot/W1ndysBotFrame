from . import *
import logger


class MetaEventHandler:
    """
    元事件处理器/定时任务处理器
    元事件可利用心跳来实现定时任务
    """

    def __init__(self, websocket, msg):
        self.websocket = websocket
        self.msg = msg
        self.time = msg.get("time", "")
        self.post_type = msg.get("post_type", "")

    async def handle(self):
        logger.info(f"[{MODULE_NAME}]收到元事件")
