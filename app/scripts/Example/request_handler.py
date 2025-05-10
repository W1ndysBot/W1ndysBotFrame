# app/scripts/Example/request_handler.py

import logging
from app.scripts.Example.data_manager import DataManager


class RequestHandler:
    """请求处理器

    负责处理:
    - 加好友请求
    - 加群请求
    """

    def __init__(self):
        """初始化请求处理器

        Args:
            data_manager: DataManager实例，用于管理数据和开关状态
        """
        try:
            # 初始化 DataManager 实例
            self.data_manager = DataManager()
            # 保存websocket连接
            self.websocket = None
            self.request_type = ""
            self.user_id = ""
            self.comment = ""
            self.flag = ""
            self.sub_type = ""
            self.group_id = ""
        except Exception as e:
            logging.error(f"[Example]初始化请求处理器失败: {e}")
            raise

    async def handle(self, msg):
        """处理所有请求类型

        根据 NapCatQQ 的上报事件类型，请求事件可以分为:
        - request.friend: 加好友请求
        - request.group.add: 加群请求
        - request.group.invite: 邀请登录号入群请求
        """
        try:
            self.request_type = msg.get("request_type", "")
            self.user_id = str(msg.get("user_id", ""))
            self.comment = msg.get("comment", "")
            self.flag = msg.get("flag", "")
            self.sub_type = msg.get("sub_type", "")
            self.group_id = msg.get("group_id", "")

            # 根据请求类型分发处理
            if self.request_type == "friend":
                await self.handle_friend_request(msg)
            elif self.request_type == "group":
                await self.handle_group_request(msg)
        except Exception as e:
            logging.error(f"[Example]分发处理请求事件失败: {e}")
            return

    async def handle_friend_request(self, msg):
        """处理加好友请求

        字段列表:
        - user_id: 请求者 QQ 号
        - comment: 验证信息
        - flag: 请求 flag，在调用处理请求的 API 时需要传入
        """
        try:
            # 实现好友请求处理逻辑
            pass
        except Exception as e:
            logging.error(f"[Example]处理好友请求失败: {e}")
            return

    async def handle_group_request(self, msg):
        """处理加群请求或邀请

        字段列表:
        - sub_type: 请求子类型，add 为请求入群，invite 为邀请登录号入群
        - group_id: 群号
        - user_id: 请求者/邀请者 QQ 号
        - comment: 验证信息/邀请信息
        - flag: 请求 flag，在调用处理请求的 API 时需要传入
        """
        try:
            # 根据子类型处理不同情况
            if self.sub_type == "add":
                # 处理加群请求
                pass
            elif self.sub_type == "invite":
                # 处理邀请登录号入群
                pass
        except Exception as e:
            logging.error(f"[Example]处理群请求失败: {e}")
            return
