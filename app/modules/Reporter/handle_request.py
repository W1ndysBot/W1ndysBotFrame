from . import MODULE_NAME, DATA_DIR, SWITCH_FILE

import logger


class RequestHandler:
    """请求处理器"""

    def __init__(self, websocket, msg):
        self.websocket = websocket
        self.msg = msg
        self.time = msg.get("time", "")
        self.request_type = msg.get("request_type", "")
        self.user_id = self.msg.get("user_id", "")
        self.comment = self.msg.get("comment", "")
        self.flag = self.msg.get("flag", "")

    async def handle_friend(self):
        """
        处理好友请求
        """
        pass

    async def handle_group(self):
        """
        处理群请求
        """
        self.sub_type = self.msg.get("sub_type", "")
        if self.sub_type == "invite":
            await self.handle_group_invite()
        elif self.sub_type == "add":
            await self.handle_group_add()
        else:
            logger.error(f"[{MODULE_NAME}]收到未知群请求类型: {self.sub_type}")

    async def handle_group_invite(self):
        """
        处理群邀请请求
        """
        pass

    async def handle_group_add(self):
        """
        处理群添加请求
        """
        pass

    async def handle(self):
        if self.request_type == "friend":
            await self.handle_friend()
        elif self.request_type == "group":
            await self.handle_group()
        else:
            logger.error(f"[{MODULE_NAME}]收到未知请求类型: {self.request_type}")
