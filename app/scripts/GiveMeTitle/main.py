# app/scripts/GiveMeTitle/main.py

import logging
import os
import sys

# 添加项目根目录到sys.path
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from app.api.message import send_group_msg, send_private_msg
from app.scripts.GiveMeTitle.data_manager import DataManager
from app.scripts.GiveMeTitle.message_handler import MessageHandler
from app.scripts.GiveMeTitle.notice_handler import NoticeHandler
from app.scripts.GiveMeTitle.request_handler import RequestHandler
from app.scripts.GiveMeTitle.response_handler import ResponseHandler


class GiveMeTitleManager:
    """示例管理类 - 使用组合模式重构

    通过组合不同的处理器，实现模块化设计，包括：
    - 数据管理器：负责数据存储和功能开关
    - 消息处理器：负责群消息和私聊消息处理
    - 通知处理器：负责各类通知事件处理
    - 请求处理器：负责加好友和加群请求处理
    - 响应处理器：负责API回调响应处理
    """

    def __init__(self):
        """初始化各个子系统"""
        try:
            # 初始化各个子系统
            self.websocket = None
            self.data_manager = DataManager()
            self.message_handler = MessageHandler()
            self.notice_handler = NoticeHandler()
            self.request_handler = RequestHandler()
            self.response_handler = ResponseHandler()
        except Exception as e:
            logging.error(f"[GiveMeTitle]初始化GiveMeTitleManager失败: {e}")
            raise

    async def handle_meta_event(self, msg):
        """处理元事件，如心跳等"""
        try:
            # 元事件处理逻辑，可用于定时任务等
            meta_type = msg.get("meta_event_type", "")

            # 处理不同类型的元事件
            if meta_type == "heartbeat":
                # 处理心跳事件，可用于定时任务
                pass
            elif meta_type == "lifecycle":
                # 处理生命周期事件
                sub_type = msg.get("sub_type", "")
                if sub_type == "connect":
                    # WebSocket连接成功
                    pass
                # 其他生命周期子类型处理
            # 可以添加更多元事件类型的处理
        except Exception as e:
            logging.error(f"[GiveMeTitle]处理元事件失败: {e}")
            return

    def get_error_type_name(self, post_type):
        """获取事件类型的中文名称"""
        try:
            return {
                "message": "消息",
                "notice": "通知",
                "request": "请求",
                "meta_event": "元事件",
            }.get(post_type or "", "未知")
        except Exception as e:
            logging.error(f"[GiveMeTitle]获取事件类型名称失败: {e}")
            return "未知"

    async def handle_events(self, websocket, msg):
        """统一事件处理入口

        通过组合模式，将不同类型的事件分发到各个专门的处理器

        Args:
            websocket: WebSocket连接对象
            msg: 接收到的消息字典
        """
        try:
            self.websocket = websocket
            # 将websocket连接传递给各处理器
            self.message_handler.websocket = self.websocket
            self.notice_handler.websocket = self.websocket
            self.request_handler.websocket = self.websocket
            self.response_handler.websocket = self.websocket

            # 处理回调事件
            if msg.get("status") == "ok":
                await self.response_handler.handle(msg)
                return

            # 基于事件类型分发到不同的处理器
            post_type = msg.get("post_type", "")

            # 处理元事件
            if post_type == "meta_event":
                await self.handle_meta_event(msg)

            # 处理消息事件
            elif post_type == "message":
                await self.message_handler.handle(msg)

            # 处理通知事件
            elif post_type == "notice":
                await self.notice_handler.handle(msg)

            # 处理请求事件
            elif post_type == "request":
                await self.request_handler.handle(msg)

        except Exception as e:
            # 获取基本事件类型用于错误日志
            post_type = msg.get("post_type", "")
            error_type = self.get_error_type_name(post_type)
            logging.error(f"[GiveMeTitle]处理GiveMeTitle{error_type}事件失败: {e}")

            # 尝试发送错误提示
            try:
                # 只有在消息类型事件中才发送错误提示
                if post_type == "message":
                    message_type = msg.get("message_type", "")
                    if message_type == "group":
                        group_id = msg.get("group_id", "")
                        if group_id:
                            await send_group_msg(
                                self.websocket,
                                group_id,
                                f"处理GiveMeTitle{error_type}事件失败，错误信息：{str(e)}",
                            )
                    elif message_type == "private":
                        user_id = str(msg.get("user_id", ""))
                        if user_id:
                            await send_private_msg(
                                self.websocket,
                                user_id,
                                f"处理GiveMeTitle{error_type}事件失败，错误信息：{str(e)}",
                            )
            except Exception as inner_e:
                # 避免在错误处理中引发新的错误
                logging.error(f"[GiveMeTitle]发送错误提示失败: {inner_e}")


# 创建示例管理器实例 - 单例模式
GiveMeTitle_manager = GiveMeTitleManager()
