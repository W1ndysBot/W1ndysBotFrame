# handlers/message_handler.py


import json
import logging
import asyncio


# 核心模块
from app.core.online_detect import Online_detect_manager

# 违禁词检测模块
from app.scripts.BanWordsPlus.main import BanWordsPlus_manager

# 示例模块
from app.scripts.Example.main import Example_manager

# 群组信息模块
from app.scripts.GroupInfo.main import GroupInfo_manager

# 群组管理模块
from app.scripts.GroupManager.main import GroupManager_manager

# 刷屏检测模块
from app.scripts.ChatSpamCheck.main import ChatSpamCheck_manager

# 问答系统模块
from app.scripts.QASystem.main import QASystem_manager


class EventHandler:
    def __init__(self):
        # 事件处理器列表
        self.handlers = [
            Online_detect_manager.handle_events,  # 在线监测
            Example_manager.handle_events,  # 示例模块
            GroupInfo_manager.handle_events,  # 群组信息模块
            GroupManager_manager.handle_events,  # 群组管理模块
            BanWordsPlus_manager.handle_events,  # 违禁词检测
            ChatSpamCheck_manager.handle_events,  # 刷屏检测
            QASystem_manager.handle_events,  # 问答系统模块
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
