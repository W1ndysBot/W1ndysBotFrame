"""
开关存储
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

# 数据根目录
DATA_ROOT_DIR = "data"


# 确保数据目录存在
os.makedirs(DATA_ROOT_DIR, exist_ok=True)


def load_switch(MODULE_NAME):
    """
    加载某模块的开关
    """
    try:
        SWITCH_PATH = os.path.join(DATA_ROOT_DIR, MODULE_NAME, "switch.json")
        os.makedirs(os.path.dirname(SWITCH_PATH), exist_ok=True)
        if os.path.exists(SWITCH_PATH):
            with open(SWITCH_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return {}
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"[{MODULE_NAME}]加载开关文件失败: {e}")
        return {}


def save_switch(switch, MODULE_NAME):
    """
    保存某模块的开关
    """
    try:
        SWITCH_PATH = os.path.join(DATA_ROOT_DIR, MODULE_NAME, "switch.json")
        os.makedirs(os.path.dirname(SWITCH_PATH), exist_ok=True)
        with open(SWITCH_PATH, "w", encoding="utf-8") as f:
            json.dump(switch, f, ensure_ascii=False, indent=2)
    except IOError as e:
        logger.error(f"[{MODULE_NAME}]保存开关文件失败: {e}")


def toggle_switch(group_id, MODULE_NAME):
    """
    切换某模块的开关
    """
    try:
        switch = load_switch(MODULE_NAME)
        switch[group_id] = not switch[group_id]
        save_switch(switch, MODULE_NAME)
        return switch[group_id]
    except Exception as e:
        logger.error(f"[{MODULE_NAME}]切换开关失败: {e}")
        return False


def get_group_all_switch(group_id):
    """
    获取某群组所有模块的开关
    返回格式为：
    {
        "group_id": {
            "module_name1": True,
            "module_name2": False
        }
    }
    """
    switch = {group_id: {}}
    # 遍历所有数据目录
    for module_name in os.listdir(DATA_ROOT_DIR):
        switch_data = load_switch(module_name)
        if group_id in switch_data.get("switch", {}):
            switch[group_id][module_name] = switch_data["switch"][group_id]
    return switch
