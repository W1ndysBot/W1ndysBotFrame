from . import *
import logger


class NoticeHandler:
    """
    通知处理器
    websocket: 连接对象
    msg: 通知消息
    相关文档: https://napneko.github.io/develop/event#notice-%E4%BA%8B%E4%BB%B6
    """

    def __init__(self, websocket, msg):
        self.websocket = websocket
        self.msg = msg
        self.time = msg.get("time", "")
        self.notice_type = msg.get("notice_type", "")
        # 后面可以根据文档来添加更多属性和函数

    async def handle(self):
        logger.info(f"[{MODULE_NAME}]收到通知")
