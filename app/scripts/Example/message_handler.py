# app/scripts/Example/message_handler.py

import logging
from api.message import send_group_msg, send_private_msg
from scripts.Example.group_message_handler import GroupMessageHandler
from scripts.Example.private_message_handler import PrivateMessageHandler
from scripts.Example.data_manager import DataManager


class MessageHandler:
    """消息处理器 - 负责消息分发

    根据消息类型将消息分发给专门的处理器:
    - GroupMessageHandler: 处理群聊消息
    - PrivateMessageHandler: 处理私聊消息
    """

    def __init__(self):
        """初始化消息处理器

        Args:
            data_manager: DataManager实例，用于管理数据和开关状态
        """
        # 初始化 DataManager 实例
        self.data_manager = DataManager()
        # 保存websocket连接
        self.websocket = None

        # 初始化专门的消息处理器
        self.group_handler = GroupMessageHandler()
        self.private_handler = PrivateMessageHandler()

    async def handle(self, msg):
        """处理所有消息类型

        根据 NapCatQQ 的上报事件类型，消息事件可以分为:
        - message.private: 私聊消息
        - message.private.friend: 好友
        - message.private.group: 群临时会话
        - message.private.group_self: 群中自身发送 (不支持)
        - message.private.other: 其他 (不支持)
        - message.group: 群聊消息
        - message.group.normal: 普通消息
        - message.group.notice: 系统提示 (不支持)
        """
        try:
            message_type = msg.get("message_type", "")

            # 分发到对应的处理器
            if message_type == "group":
                # 群聊消息处理
                self.group_handler.websocket = self.websocket
                await self.group_handler.handle(msg)
            elif message_type == "private":
                # 私聊消息处理
                self.private_handler.websocket = self.websocket
                await self.private_handler.handle(msg)
            else:
                # 未知消息类型
                logging.warning(f"未知的消息类型: {message_type}")

        except Exception as e:
            # 处理分发过程中的异常
            logging.error(f"消息分发失败: {e}")

            # 尝试发送错误通知
            try:
                message_type = msg.get("message_type", "")
                if message_type == "group":
                    group_id = msg.get("group_id", "")
                    if group_id:
                        await send_group_msg(
                            self.websocket,
                            group_id,
                            f"消息处理失败，错误信息：{str(e)}",
                        )
                elif message_type == "private":
                    user_id = str(msg.get("user_id", ""))
                    if user_id:
                        await send_private_msg(
                            self.websocket,
                            user_id,
                            f"消息处理失败，错误信息：{str(e)}",
                        )
            except Exception as inner_e:
                logging.error(f"发送错误通知失败: {inner_e}")

            return
