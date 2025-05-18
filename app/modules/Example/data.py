"""
数据存储
"""

import os

# 数据根目录
DATA_ROOT_DIR = "data"

# 模块目录
MODULE_DIR = "Example"

# 数据目录
DATA_DIR = os.path.join(DATA_ROOT_DIR, MODULE_DIR)

# 开关文件路径
SWITCH_PATH = os.path.join(DATA_DIR, "switch.json")

# 确保数据目录存在
os.makedirs(DATA_DIR, exist_ok=True)
