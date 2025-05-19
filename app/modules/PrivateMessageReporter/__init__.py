import os

# 模块名称
MODULE_NAME = "PrivateMessageReporter"

# 模块描述
MODULE_DESCRIPTION = "私聊转达"

# 数据目录
DATA_DIR = os.path.join("data", MODULE_NAME)
os.makedirs(DATA_DIR, exist_ok=True)

# 开关文件
SWITCH_FILE = os.path.join(DATA_DIR, "switch.json")
