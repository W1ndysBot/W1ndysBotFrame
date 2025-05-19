import os
from core.switchs import load_switch, toggle_switch

# 模块名称
MODULE_NAME = "template"

# 模块描述
MODULE_DESCRIPTION = "模板模块"

# 数据目录
DATA_DIR = os.path.join("data", MODULE_NAME)
os.makedirs(DATA_DIR, exist_ok=True)

# 开关文件
SWITCH_FILE = os.path.join(DATA_DIR, "switch.json")

# 加载开关
load_switch(MODULE_NAME)


# 切换群聊开关
def toggle_group_switch(group_id, MODULE_NAME):
    toggle_switch("group", group_id, MODULE_NAME)


# 切换私聊开关
def toggle_private_switch(MODULE_NAME):
    toggle_switch("private", MODULE_NAME)
