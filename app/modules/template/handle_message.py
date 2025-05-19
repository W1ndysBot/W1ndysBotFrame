from . import *
import logger


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
        try:
            self.group_id = str(self.msg.get("group_id", ""))  # 群号
            self.message_id = str(self.msg.get("message_id", ""))  # 消息ID
            self.user_id = str(self.msg.get("user_id", ""))  # 发送者QQ号
            self.message = self.msg.get("message", {})  # 消息段数组
            self.raw_message = self.msg.get("raw_message", "")  # 原始消息
            self.sender = self.msg.get("sender", {})  # 发送者信息
        except Exception as e:
            logger.error(f"[{MODULE_NAME}]处理群消息失败: {e}")

    async def handle_private(self):
        """
        处理私聊消息
        """
        try:
            pass
        except Exception as e:
            logger.error(f"[{MODULE_NAME}]处理私聊消息失败: {e}")

    async def handle(self):
        if self.message_type == "group":
            await self.handle_group()
        elif self.message_type == "private":
            await self.handle_private()
