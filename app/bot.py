# bot.py

import logging
import asyncio
import websockets
import config
from datetime import datetime
from handler_events import event_handler
from api.message import send_private_msg


class Bot:
    def __init__(self, ws_url=None, token=None, owner_id=None):
        # 使用传入的参数或配置文件中的默认值
        self.ws_url = ws_url or config.ws_url
        self.token = token or config.token
        self.owner_id = owner_id or config.owner_id
        self.tasks = set()  # 用于存储所有任务的集合
        self.websocket = None
        self.last_notify_time = 0  # 上次发送上线通知的时间戳

    async def process_message(self, websocket, message):
        """处理接收到的消息"""
        try:
            self.websocket = websocket
            await event_handler.handle_message(websocket, message)
        except Exception as e:
            # 添加更详细的错误日志
            logging.error(f"处理websocket消息时出错: {e}")
            logging.error(f"websocket消息内容: {message}")
            # 可选：将错误通知发送给机器人所有者
            try:
                tasks = [
                    send_private_msg(
                        self.websocket,
                        owner,
                        f"处理websocket消息时出错: {e}\nwebsocket消息内容: {message}",
                    )
                    for owner in self.owner_id
                ]
                await asyncio.gather(*tasks)
            except Exception as notify_error:
                logging.error(f"发送错误通知失败: {notify_error}")

    def clean_tasks(self):
        """清理已完成的任务"""
        done = {t for t in self.tasks if t.done()}
        self.tasks.difference_update(done)
        for t in done:
            try:
                t.result()
            except Exception as e:
                # 添加更详细的错误日志
                logging.error(f"任务执行出错: {e}")
                logging.exception("详细错误信息:")

    async def connect(self):
        """连接到机器人并开始接收消息"""
        logging.info("正在连接到机器人...")
        logging.info(f"连接地址: {self.ws_url}")

        # 如果URL中包含token，直接使用URL中的token
        if self.token and "access_token=" not in self.ws_url:
            # 检查原始URL是否已经包含参数
            if "?" in self.ws_url:
                ws_url = f"{self.ws_url}&access_token={self.token}"
            else:
                ws_url = f"{self.ws_url}?access_token={self.token}"
            logging.info(f"添加token参数后的连接地址: {ws_url}")
        else:
            ws_url = self.ws_url

        try:
            # 直接连接，将token作为URL参数
            async with websockets.connect(ws_url) as websocket:
                return await self._handle_connection(websocket)
        except Exception as e:
            logging.error(f"WebSocket连接失败: {e}")
            return None

    async def _handle_connection(self, websocket):
        """处理连接后的消息接收和处理"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"已连接到机器人。当前时间: {current_time}")

        async for message in websocket:
            # 清理已完成的任务
            self.clean_tasks()
            # 创建新任务并添加到任务集合
            task = asyncio.create_task(self.process_message(websocket, message))
            self.tasks.add(task)


# 创建全局实例
bot = Bot()
