# app/scripts/Example/private_message_handler.py

import logging
from app.api.message import send_private_msg
from app.scripts.Example.data_manager import DataManager


class PrivateMessageHandler:
    """私聊消息处理器

    专门负责处理:
    - 好友私聊消息
    - 群临时会话消息
    - 其他来源私聊消息
    """

    def __init__(self):
        """初始化私聊消息处理器

        Args:
            data_manager: DataManager实例，用于管理数据和开关状态
        """
        try:
            # 初始化 DataManager 实例
            self.data_manager = DataManager()
            # 保存websocket连接
            self.websocket = None
            self.user_id = ""
            self.message_id = ""
            self.raw_message = ""
            self.sub_type = ""
            self.sender = {}
            self.message = ""
        except Exception as e:
            logging.error(f"[Example]初始化私聊消息处理器失败: {e}")
            raise

    async def handle(self, msg):
        """处理私聊消息

        处理消息类型:
        - message.private.friend: 好友私聊
        - message.private.group: 群临时会话

        字段列表:
        - user_id: 发送者 QQ 号
        - message_id: 消息 ID
        - message: 消息内容
        - raw_message: 原始消息内容
        - sender: 发送者信息
        - sub_type: 消息子类型，可能为 friend, group 等
        - temp_source: 临时会话来源
        """
        try:
            self.user_id = str(msg.get("user_id", ""))
            self.message_id = str(msg.get("message_id", ""))
            self.raw_message = str(msg.get("raw_message", ""))
            self.sub_type = str(msg.get("sub_type", ""))
            self.sender = msg.get("sender", {})
            self.message = msg.get("message", "")

            # 根据消息子类型分别处理
            if self.sub_type == "friend":
                await self._handle_friend_message()
            elif self.sub_type == "group":
                await self._handle_temp_message()
            else:
                # 处理其他类型的私聊
                await self._handle_other_private_message()

        except Exception as e:
            logging.error(f"[Example]处理私聊消息失败: {e}")
            user_id = str(msg.get("user_id", ""))
            if user_id:
                await send_private_msg(
                    self.websocket,
                    user_id,
                    f"处理私聊消息失败，错误信息：{str(e)}",
                )
            return

    async def _handle_friend_message(self):
        """处理好友私聊消息"""
        try:
            # 使用已存储的类属性
            # 在这里添加更多好友私聊功能
            pass
        except Exception as e:
            logging.error(f"[Example]处理好友私聊消息失败: {e}")
            if self.user_id:
                await send_private_msg(
                    self.websocket,
                    self.user_id,
                    f"处理好友私聊消息失败，错误信息：{str(e)}",
                )
            return

    async def _handle_temp_message(self):
        """处理临时会话消息"""
        try:

            # 在这里添加更多临时会话处理逻辑
            pass
        except Exception as e:
            logging.error(f"[Example]处理临时会话消息失败: {e}")
            if self.user_id:
                await send_private_msg(
                    self.websocket,
                    self.user_id,
                    f"处理临时会话消息失败，错误信息：{str(e)}",
                )
            return

    async def _handle_other_private_message(self):
        """处理其他来源的私聊消息"""
        try:
            # 使用已存储的类属性
            logging.info(
                f"收到其他来源私聊消息，类型: {self.sub_type}, 用户: {self.user_id}"
            )

            # 简单回复
            await send_private_msg(
                self.websocket,
                self.user_id,
                "已收到您的消息，但暂不支持此类型的会话处理。",
            )
            return
        except Exception as e:
            logging.error(f"[Example]处理其他来源私聊消息失败: {e}")
            if self.user_id:
                await send_private_msg(
                    self.websocket,
                    self.user_id,
                    f"处理其他来源私聊消息失败，错误信息：{str(e)}",
                )
            return
