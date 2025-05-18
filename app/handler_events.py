# handlers/message_handler.py


import json
import logging
import asyncio


# 核心模块
from core.online_detect import Online_detect_manager

# 示例模块
from scripts.Example.main import handle_events as example_handle_events


class EventHandler:
    def __init__(self):
        # 事件处理器列表
        self.handlers = [
            Online_detect_manager.handle_events,  # 在线监测
            example_handle_events,  # 示例模块
        ]

    async def handle_message(self, websocket, message):
        """处理websocket消息"""
        try:
            msg = json.loads(message)
            logging.info(f"{'*' * 100}\n收到事件：{msg}\n{'*' * 100}\n\n")
            # 并发调用各个模块的事件处理器
            tasks = [handler(websocket, msg) for handler in self.handlers]
            await asyncio.gather(*tasks)

        except Exception as e:
            logging.error(f"处理websocket消息的逻辑错误: {e}")


# 创建全局实例
event_handler = EventHandler()
