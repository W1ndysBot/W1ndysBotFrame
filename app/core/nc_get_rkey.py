import logger
from config import OWNER_ID
from api.key import nc_get_rkey
from api.message import send_private_msg
import re
import os
import json
import time

DATA_DIR = os.path.join("data", "Core", "nc_get_rkey.json")

# 全局变量，记录上次请求时间
last_request_time = 0
REQUEST_INTERVAL = 600  # 10分钟，单位：秒


# 如果字符串中有图片（包含rkey），则替换为本地缓存的rkey
def replace_rkey_match(match):
    """
    替换匹配对象中的rkey参数
    """
    try:
        cq_img = match.group(0)
        # 查找rkey参数
        rkey_pattern = r"rkey=([^,^\]]+)"
        rkey_search = re.search(rkey_pattern, cq_img)
        if rkey_search:
            # 读取本地rkey
            with open(DATA_DIR, "r", encoding="utf-8") as f:
                rkey_json = json.load(f)
            new_rkey = rkey_json.get("rkey")
            if new_rkey:
                # 替换rkey参数
                new_cq_img = re.sub(rkey_pattern, f"rkey={new_rkey}", cq_img)
                return new_cq_img
    except Exception as e:
        logger.error(f"本地rkey替换失败: {e}")
    return match.group(0)


def replace_rkey(text):
    """
    在文本中查找并替换所有包含rkey的CQ图片码
    参数:
        text: str 包含可能的CQ图片码的文本
    返回:
        str 替换后的文本
    """
    try:
        if not text or not isinstance(text, str):
            return text

        # 查找所有CQ图片码模式，包含rkey参数的
        cq_img_pattern = r"\[CQ:image,[^\]]*rkey=[^\]]*\]"

        # 使用re.sub替换所有匹配的图片码
        result = re.sub(cq_img_pattern, replace_rkey_match, text)
        return result
    except Exception as e:
        logger.error(f"替换rkey失败: {e}")
        return text


def save_rkey_to_file(item):
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
        "status": "ok",
        "retcode": 0,
        "data": [
            {
                "rkey": "string",
                "ttl": "string",
                "time": 0,
                "type": 0
            }
        ],
        "message": "string",
        "wording": "string",
        "echo": "string"
    }
    """
    global last_request_time
    try:
        current_time = int(time.time())
        # 检查距离上次请求是否已超过10分钟
        if current_time - last_request_time >= REQUEST_INTERVAL:
            # 发送nc_get_rkey请求
            await nc_get_rkey(websocket)
            last_request_time = current_time

        if msg.get("status") == "ok":
            echo = msg.get("echo", "")
            # 格式：nc_get_rkey
            match = re.search(r"nc_get_rkey", echo)
            if match:
                data_list = msg.get("data", [])
                if isinstance(data_list, list) and len(data_list) > 0:
                    for item in data_list:
                        rkey = item.get("rkey")
                        ttl = item.get("ttl")
                        rkey_time = item.get("time")
                        rkey_type = item.get("type")
                        # 保存到文件
                        save_rkey_to_file(item)
                        logger.success(
                            f"获取到nc_get_rkey: rkey={rkey}, ttl={ttl}, time={rkey_time}, type={rkey_type}，已保存到文件"
                        )
                else:
                    logger.warning("未获取到有效的rkey数据列表")
    except Exception as e:
        logger.error(f"自动刷新rkey失败: {e}")
        await send_private_msg(websocket, OWNER_ID, f"自动刷新rkey失败: {e}")
