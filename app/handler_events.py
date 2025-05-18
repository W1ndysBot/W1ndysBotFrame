# handlers/message_handler.py


import json
import asyncio
import logger


# 核心模块
from core.online_detect import handle_events as online_detect_handle_events

# 示例模块
from scripts.Example.main import handle_events as example_handle_events


class EventHandler:
    def __init__(self):
        # 事件处理器列表
        self.handlers = [
            online_detect_handle_events,  # 在线监测
            example_handle_events,  # 示例模块
        ]

    async def handle_message(self, websocket, message):
        """处理websocket消息"""
        try:
            msg = json.loads(message)

            # 打印WebSocket消息
            logger.info("=" * 50)
            logger.info("📩 收到WebSocket消息:")
            logger.info(msg)
            logger.info("=" * 50)

            # 并发调用各个模块的事件处理器
            tasks = [handler(websocket, msg) for handler in self.handlers]
            await asyncio.gather(*tasks)

        except Exception as e:
            logger.error(f"处理websocket消息的逻辑错误: {e}")
