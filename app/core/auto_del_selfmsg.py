"""
自动撤回自己发送的消息
"""

import logger
import re
import asyncio
from api.message import delete_msg


async def del_self_msg(websocket, msg_id, del_time):
    """
    定时撤回消息
    """
    await asyncio.sleep(del_time)
    await delete_msg(websocket, msg_id)


async def handle_events(websocket, msg):
    """
    处理回应事件
    """
    try:
        if msg.get("status") == "ok":
            echo = msg.get("echo", {})
            # 格式：(秒)秒撤回(消息ID)消息
            res = re.search(r"(\d+)秒撤回(\d+)消息", echo.get("data", ""))
            if res:
                del_time = int(res.group(1))
                msg_id = int(res.group(2))
                if del_time > 0:
                    # 新开一个线程，定时撤回消息
                    asyncio.create_task(del_self_msg(websocket, msg_id, del_time))
    except Exception as e:
        logger.error(f"自动撤回自己发送的消息失败: {e}")
