# script/example/main.py

import logging
import os
import sys

# 添加项目根目录到sys.path
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from app.config import *
from app.api import *
from app.switch import load_switch, save_switch

# 数据存储路径，实际开发时，请将Example替换为具体的数据存放路径
DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data",
    "Example",
)


# 查看功能开关状态
def load_function_status(group_id):
    return load_switch(group_id, "example")


# 保存功能开关状态
def save_function_status(group_id, status):
    save_switch(group_id, "example", status)


# 群消息处理函数
async def handle_Example_group_message(websocket, msg):
    # 确保数据目录存在
    os.makedirs(DATA_DIR, exist_ok=True)
    try:
        user_id = str(msg.get("user_id"))
        group_id = str(msg.get("group_id"))
        raw_message = str(msg.get("raw_message"))
        role = str(msg.get("sender", {}).get("role"))
        message_id = str(msg.get("message_id"))

    except Exception as e:
        logging.error(f"处理Example群消息失败: {e}")
        await send_group_msg(
            websocket,
            group_id,
            "处理Example群消息失败，错误信息：" + str(e),
        )
        return


# 群通知处理函数
async def handle_Example_group_notice(websocket, msg):
    # 确保数据目录存在
    os.makedirs(DATA_DIR, exist_ok=True)
    try:
        user_id = str(msg.get("user_id"))
        group_id = str(msg.get("group_id"))
        raw_message = str(msg.get("raw_message"))
        role = str(msg.get("sender", {}).get("role"))
        message_id = str(msg.get("message_id"))

    except Exception as e:
        logging.error(f"处理Example群通知失败: {e}")
        await send_group_msg(
            websocket,
            group_id,
            "处理Example群通知失败，错误信息：" + str(e),
        )
        return
