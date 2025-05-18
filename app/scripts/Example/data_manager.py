# app/scripts/Example/data_manager.py

import os
import json
import logging

from config import owner_id


class DataManager:
    """Example模块数据管理类

    负责:
    - 功能开关状态管理
    - 数据存储和读取
    - 权限检查
    """

    def __init__(self):
        try:

            # 数据根目录
            self.DATA_ROOT_DIR = os.path.join(
                os.path.dirname(
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                ),
                "data",
            )

            # 数据存储路径
            self.DATA_DIR = os.path.join(self.DATA_ROOT_DIR, "Example")
            # 群组开关数据目录
            self.SWITCH_DATA_DIR = os.path.join(self.DATA_ROOT_DIR, "GroupSwitch")
            # 群组信息数据目录
            self.GROUP_INFO_DATA_DIR = os.path.join(self.DATA_ROOT_DIR, "GroupInfo")

            # 确保数据目录存在
            os.makedirs(self.DATA_ROOT_DIR, exist_ok=True)
            os.makedirs(self.DATA_DIR, exist_ok=True)
            os.makedirs(self.SWITCH_DATA_DIR, exist_ok=True)
            os.makedirs(self.GROUP_INFO_DATA_DIR, exist_ok=True)

        except Exception as e:
            logging.error(f"[Example]初始化数据管理器失败: {e}")
            raise

    def load_switch(self, group_id, key):
        """加载群组开关"""
        try:
            with open(
                os.path.join(self.SWITCH_DATA_DIR, f"{group_id}.json"),
                "r",
                encoding="utf-8",
            ) as f:
                switches = json.load(f)
        except FileNotFoundError:
            # 创建文件并写入空字典
            switches = {}
            with open(
                os.path.join(self.SWITCH_DATA_DIR, f"{group_id}.json"),
                "w",
                encoding="utf-8",
            ) as f:
                json.dump(switches, f, ensure_ascii=False, indent=4)

        return switches.get(key, False)

    def save_switch(self, group_id, key, switch):
        """保存群组开关"""
        try:
            with open(
                os.path.join(self.SWITCH_DATA_DIR, f"{group_id}.json"),
                "r",
                encoding="utf-8",
            ) as f:
                switches = json.load(f)
        except FileNotFoundError:
            switches = {}

        switches[key] = switch

        with open(
            os.path.join(self.SWITCH_DATA_DIR, f"{group_id}.json"),
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(switches, f, ensure_ascii=False, indent=4)

    def load_function_status(self, group_id):
        """查看功能开关状态"""
        try:
            return self.load_switch(group_id, "Example")
        except Exception as e:
            logging.error(f"[Example]加载功能状态失败, group_id={group_id}: {e}")
            return False  # 默认返回关闭状态

    def save_function_status(self, group_id, status):
        """保存功能开关状态"""
        try:
            self.save_switch(group_id, "Example", status)
            return True
        except Exception as e:
            logging.error(f"[Example]保存功能状态失败, group_id={group_id}: {e}")
            return False

    def is_admin_or_owner(self, role):
        """检查用户是否是管理员或群主"""
        return role in ["owner", "admin"]

    def is_authorized(self, user_id):
        """检查用户是否有权限操作"""
        try:
            return user_id in owner_id if user_id else False
        except Exception as e:
            logging.error(f"[Example]检查用户权限失败, user_id={user_id}: {e}")
            return False  # 出错时默认拒绝权限

    def save_data(self, filename, data):
        """保存数据到JSON文件"""
        try:
            file_path = os.path.join(self.DATA_DIR, filename)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            logging.error(f"[Example]保存数据失败 {filename}: {e}")
            return False

    def load_data(self, filename, default=None):
        """从JSON文件加载数据"""
        try:
            file_path = os.path.join(self.DATA_DIR, filename)
            if not os.path.exists(file_path):
                return default if default is not None else []

            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"[Example]加载数据失败 {filename}: {e}")
            return default if default is not None else []
