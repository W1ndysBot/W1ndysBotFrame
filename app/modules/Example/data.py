"""
数据存储
每个模块的开关群记录和数据都存储在data/module_name目录下
开关文件为switch.json，存储结构为：
{
    "switch": {
        "群号1": True,
        "群号2": False
    }
}

"""

import os
import json
import logger
from . import MODULE_NAME

# 数据根目录
DATA_ROOT_DIR = "data"


# 数据目录
DATA_DIR = os.path.join(DATA_ROOT_DIR, MODULE_NAME)

# 开关文件路径
SWITCH_PATH = os.path.join(DATA_DIR, "switch.json")

# 确保数据目录存在
os.makedirs(DATA_DIR, exist_ok=True)


def load_switch():
    """
    加载开关
    """
    try:
        if os.path.exists(SWITCH_PATH):
            with open(SWITCH_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return {}
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"[{MODULE_NAME}]加载开关文件失败: {e}")
        return {}


def save_switch(switch):
    """
    保存开关
    """
    try:
        with open(SWITCH_PATH, "w", encoding="utf-8") as f:
            json.dump(switch, f, ensure_ascii=False, indent=2)
    except IOError as e:
        logger.error(f"[{MODULE_NAME}]保存开关文件失败: {e}")
