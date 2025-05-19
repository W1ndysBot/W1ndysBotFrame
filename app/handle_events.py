import json
import asyncio
import logger
import shutil

# 核心模块
from core.online_detect import handle_events as online_detect_handle_events  # 在线监测
from core.logs_clean import clean_logs  # 日志清理

# 模板模块
from modules.template.main import handle_events as template_handle_events


class EventHandler:
    def __init__(self):

        # 事件处理器列表
        self.handlers = [
            clean_logs,  # 日志清理
            online_detect_handle_events,  # 在线监测
            template_handle_events,  # 模板模块
            ...,  # 在这里注册新的模块
        ]

    async def handle_message(self, websocket, message):
        """处理websocket消息"""
        try:
            msg = json.loads(message)

            # 打印WebSocket消息
            terminal_width = shutil.get_terminal_size().columns
            logger.info(
                f"{'-' * terminal_width}\n📩 收到WebSocket消息:\n{msg}\n{'-' * terminal_width}"
            )

            # 并发调用各个模块的事件处理器
            tasks = [handler(websocket, msg) for handler in self.handlers]
            await asyncio.gather(*tasks)

        except Exception as e:
            logger.error(f"处理websocket消息的逻辑错误: {e}")
