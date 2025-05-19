from . import *
import logger
from core.auth import is_owner
from api.message import send_private_msg
from api.user import set_friend_add_request
from api.generate import generate_reply_message, generate_text_message
import re


class PrivateMessageHandler:
    """私聊消息处理器"""

    def __init__(self, websocket, msg):
        self.websocket = websocket
        self.msg = msg
        self.time = msg.get("time", "")
        self.sub_type = msg.get("sub_type", "")  # 子类型,friend/group
        self.user_id = str(msg.get("user_id", ""))  # 发送者QQ号
        self.message_id = str(msg.get("message_id", ""))  # 消息ID
        self.message = msg.get("message", {})  # 消息段数组
        self.raw_message = msg.get("raw_message", "")  # 原始消息
        self.sender = msg.get("sender", {})  # 发送者信息
        self.nickname = self.sender.get("nickname", "")  # 昵称

    async def handle(self):
        """
        处理私聊消息
        """
        try:
            if self.raw_message.lower() == MODULE_NAME.lower():
                switch_status = toggle_private_switch(MODULE_NAME)
                switch_status = "开启" if switch_status else "关闭"
                reply_message = generate_reply_message(self.message_id)
                text_message = generate_text_message(
                    f"[{MODULE_NAME}]私聊开关已切换为【{switch_status}】"
                )
                await send_private_msg(
                    self.websocket,
                    self.user_id,
                    [reply_message, text_message],
                )
                return

            # 如果没开启私聊开关，则不处理
            if not load_switch(MODULE_NAME)["private"]:
                return

            # 鉴权
            if not is_owner(self.user_id):
                return

            # 处理好友请求
            # 格式: 同意/拒绝+请求ID
            if re.match(r"^(同意|拒绝)\s+\d+$", self.raw_message):
                # 提取行为和请求ID
                parts = self.raw_message.split(" ")
                action = parts[0]
                flag = parts[1]
                # 处理好友请求
                approve = action == "同意"
                await set_friend_add_request(self.websocket, flag, approve)
                reply_message = generate_reply_message(self.message_id)
                text_message = generate_text_message(f"[{MODULE_NAME}]已处理好友请求")
                await send_private_msg(
                    self.websocket, self.user_id, [reply_message, text_message]
                )
                return

        except Exception as e:
            logger.error(f"[{MODULE_NAME}]处理私聊消息失败: {e}")
