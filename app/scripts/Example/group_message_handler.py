# app/scripts/Example/group_message_handler.py

import logging
from api.message import send_group_msg
from api.generate import *
from scripts.Example.data_manager import DataManager


class GroupMessageHandler:
    """群聊消息处理器

    专门负责处理:
    - 群聊普通消息
    - 群聊系统提示 (不支持)
    - 群功能开关切换
    """

    def __init__(self):
        """初始化群聊消息处理器"""
        try:
            # 初始化 DataManager 实例
            self.data_manager = DataManager()
            # 保存websocket连接
            self.websocket = None
            self.group_id = ""
            self.user_id = ""
            self.message_id = ""
            self.raw_message = ""
            self.sub_type = ""
            self.sender = {}
            self.message = ""
            # 开关状态初始为None，表示尚未加载
            self.switch_status = None

        except Exception as e:
            logging.error(f"[Example]初始化群聊消息处理器失败: {e}")
            raise

    async def handle(self, msg):
        """处理群聊消息

        处理消息类型: message.group.normal
        字段列表:
        - group_id: 群号
        - user_id: 发送者 QQ 号
        - message_id: 消息 ID
        - message: 消息内容
        - raw_message: 原始消息内容
        - sender: 发送者信息
        - sub_type: 消息子类型，normal 或 notice
        """
        try:
            self.group_id = str(msg.get("group_id", ""))
            self.user_id = str(msg.get("user_id", ""))
            self.message_id = str(msg.get("message_id", ""))
            self.raw_message = str(msg.get("raw_message", ""))
            self.sub_type = str(msg.get("sub_type", "normal"))
            self.sender = msg.get("sender", {})
            self.message = msg.get("message", [])

            # 只处理普通群聊消息
            if self.sub_type != "normal":
                return

            # 在这里加载当前群的开关状态
            self.switch_status = self.data_manager.load_function_status(self.group_id)

            # 处理开关命令
            if self.raw_message.lower() == "example":
                await self.toggle_function_status()
                return

            # 检查功能是否开启
            if self.switch_status:
                # 处理群消息的主要逻辑
                await self._process_group_message()

        except Exception as e:
            logging.error(f"[Example]处理群聊消息失败: {e}")
            if self.group_id:
                await send_group_msg(
                    self.websocket,
                    self.group_id,
                    f"[Example]处理群聊消息失败，错误信息：{str(e)}",
                )
            return

    async def toggle_function_status(self):
        """处理功能开关状态切换"""
        try:
            # 检查用户权限
            if not self.data_manager.is_authorized(self.user_id):
                return

            # 切换功能状态
            current_status = self.data_manager.load_function_status(self.group_id)
            new_status = not current_status
            self.switch_status = new_status
            self.data_manager.save_function_status(self.group_id, new_status)

            # 准备回复消息
            status_text = (
                "✅✅✅Example功能已开启" if new_status else "🚫🚫🚫Example功能已关闭"
            )

            message = generate_reply_message(self.message_id) + generate_text_message(
                status_text
            )
            logging.info(f"[Example]切换功能状态成功, 开关状态: {self.switch_status}")
            # 发送状态变更通知
            await send_group_msg(
                self.websocket,
                self.group_id,
                message,
            )

        except Exception as e:
            logging.error(f"[Example]切换功能状态失败: {e}")
            if self.group_id:
                await send_group_msg(
                    self.websocket,
                    self.group_id,
                    f"切换功能状态失败，错误信息：{str(e)}",
                )
            return

    async def _process_group_message(self):
        """处理群聊消息的主要逻辑

        这里放置具体的群聊消息处理功能
        """
        try:
            # 消息字段已在handle方法中获取，无需再次获取
            # 直接使用类属性即可

            # 在这里添加更多的群聊消息处理逻辑
            pass
        except Exception as e:
            logging.error(f"[Example]处理群聊消息主要逻辑失败: {e}")
            if self.group_id:
                await send_group_msg(
                    self.websocket,
                    self.group_id,
                    f"[Example]处理群聊消息失败，错误信息：{str(e)}",
                )
            return
