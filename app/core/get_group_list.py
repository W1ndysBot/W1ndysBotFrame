import logger
from config import OWNER_ID
from api.group import get_group_list
from api.message import send_private_msg
import os
import json
import time

DATA_DIR = os.path.join("data", "Core", "get_group_list.json")

# 全局变量，记录上次请求时间
last_request_time = 0
REQUEST_INTERVAL = 3600  # 1小时，单位：秒


def save_group_list_to_file(item):
    """
    保存rkey信息到文件，确保文件夹存在
    """
    dir_path = os.path.dirname(DATA_DIR)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)
    with open(DATA_DIR, "w", encoding="utf-8") as f:
        json.dump(item, f, ensure_ascii=False, indent=2)


async def handle_events(websocket, msg):
    """
    处理回应事件
    响应示例:
    {
      "status": "ok",  // 状态，"ok"表示成功
      "retcode": 0,    // 返回码，0通常表示成功
      "data": [        // 包含多个群组信息的数组
        {
          "group_all_shut": 0,         // 群禁言状态，0表示未全员禁言，1表示已全员禁言，-1表示未知或不适用（例如，比赛群可能不会有传统禁言）
          "group_remark": "",          // 群备注名
          "group_id": "********",      // 群号 (已脱敏)
          "group_name": "********",    // 群名称 (已脱敏)
          "member_count": 41,          // 当前群成员数量
          "max_member_count": 200      // 群最大成员数量限制
        }
      ],
      "message": "",               // 状态消息，通常在出错时包含错误信息
      "wording": "",               // 补充信息或提示
      "echo": null                 // 回显字段，通常用于请求和响应的匹配
    }
    """
    global last_request_time
    try:
        current_time = int(time.time())
        # 检查距离上次请求是否已超过指定时间
        if current_time - last_request_time >= REQUEST_INTERVAL:
            # 发送获取群列表的请求
            await get_group_list(websocket, no_cache=True)
            last_request_time = current_time

        # 如果有修改群名的通知
        if msg.get("sub_type") == "group_name":
            # 发送获取群列表的请求
            await get_group_list(websocket, no_cache=True)
            last_request_time = current_time

        if msg.get("status") == "ok":
            echo = msg.get("echo", "")
            if echo == "get_group_list":
                # 保存data
                save_group_list_to_file(msg.get("data", []))
                logger.success(f"[Core]已保存群列表")
    except Exception as e:
        logger.error(f"[Core]获取群列表失败: {e}")
        await send_private_msg(websocket, OWNER_ID, f"[Core]获取群列表失败: {e}")
