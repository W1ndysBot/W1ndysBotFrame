import json
import asyncio
import logger
import shutil

# 工具模块
from utils.logs_clean import clean_logs  # 日志清理

# 核心模块
from core.online_detect import handle_events as online_detect_handle_events  # 在线监测

# 模板模块
from modules.template.main import handle_events as template_handle_events

# 上报模块
from modules.reporter.main import handle_events as reporter_handle_events


class EventHandler:
    def __init__(self):

        # 事件处理器列表
        self.handlers = [
            # 底层模块
            # ----------------------------------------------------
            clean_logs,  # 日志清理
            online_detect_handle_events,  # 在线监测
            # ----------------------------------------------------
            # 功能模块
            template_handle_events,  # 模板模块
            reporter_handle_events,  # 报告模块
            # ----------------------------------------------------
            # 在这里注册新的模块
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
