import os
from core.switchs import load_switch, toggle_switch
import logger

# 模块名称
MODULE_NAME = "reporter"

# 模块描述
MODULE_DESCRIPTION = (
    "通知报告模块，主要用于把私聊bot、加bot为好友，邀请bot入群等操作的通知报告"
)

# 数据目录
DATA_DIR = os.path.join("data", MODULE_NAME)
os.makedirs(DATA_DIR, exist_ok=True)

# 开关文件
SWITCH_FILE = os.path.join(DATA_DIR, "switch.json")

# 加载开关
load_switch(MODULE_NAME)


# 切换群聊开关
def toggle_group_switch(group_id, MODULE_NAME):
    try:
        switch_status = toggle_switch("group", group_id, MODULE_NAME)
        logger.info(f"[{MODULE_NAME}]群聊开关已切换为【{switch_status}】")
        return switch_status
    except Exception as e:
        logger.error(f"[{MODULE_NAME}]切换群聊开关失败: {e}")
        return False


# 切换私聊开关
def toggle_private_switch(MODULE_NAME):
    try:
        switch_status = toggle_switch("private", MODULE_NAME)
        logger.info(f"[{MODULE_NAME}]私聊开关已切换为【{switch_status}】")
        return switch_status
    except Exception as e:
        logger.error(f"[{MODULE_NAME}]切换私聊开关失败: {e}")
        return False
