# config.py

import json
import os
import time
import logging
from typing import Any, Dict, List, Optional, Union


class Config:
    def __init__(self):
        self.config_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "config.json"
        )
        self.last_modified_time = 0
        self.config_data: Dict[str, Any] = {}
        # 默认配置值
        self.defaults = {
            "owner_id": ["2769731875"],
            "ws_url": "ws://127.0.0.1:3001",
            "token": None,
            "DD_BOT_TOKEN": "dingtalk_token",
            "DD_BOT_SECRET": "dingtalk_secret",
        }
        self.load_config()

    def load_config(self) -> None:
        """从配置文件加载配置"""
        try:
            # 如果文件不存在，创建默认配置文件
            if not os.path.exists(self.config_path):
                self._create_default_config()
                return

            current_modified_time = os.path.getmtime(self.config_path)
            # 只有当文件被修改时才重新加载
            if current_modified_time > self.last_modified_time:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    self.config_data = json.load(f)
                self.last_modified_time = current_modified_time
                logging.info(
                    f"配置已重新加载，修改时间: {time.ctime(current_modified_time)}"
                )
        except json.JSONDecodeError as e:
            logging.error(f"JSON格式错误: {e}")
            # 如果配置文件损坏，重新创建默认配置
            self._create_default_config()
        except Exception as e:
            logging.error(f"加载配置文件失败: {e}")

    def _create_default_config(self) -> None:
        """创建默认配置文件"""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.defaults, f, indent=4, ensure_ascii=False)
            self.config_data = self.defaults.copy()
            self.last_modified_time = os.path.getmtime(self.config_path)
            logging.info(f"已创建默认配置文件: {self.config_path}")
        except Exception as e:
            logging.error(f"创建默认配置文件失败: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """通用获取配置项的方法"""
        self.load_config()
        return self.config_data.get(key, self.defaults.get(key, default))

    @property
    def owner_id(self) -> List[str]:
        return self.get("owner_id")

    @property
    def ws_url(self) -> str:
        return self.get("ws_url")

    @property
    def token(self) -> Optional[str]:
        return self.get("token")

    @property
    def DD_BOT_TOKEN(self) -> str:
        return self.get("DD_BOT_TOKEN")

    @property
    def DD_BOT_SECRET(self) -> str:
        return self.get("DD_BOT_SECRET")

    def update_config(self, key: str, value: Any) -> bool:
        """更新配置并保存到文件"""
        try:
            self.load_config()
            self.config_data[key] = value
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config_data, f, indent=4, ensure_ascii=False)
            self.last_modified_time = os.path.getmtime(self.config_path)
            logging.info(f"配置项 {key} 已更新")
            return True
        except Exception as e:
            logging.error(f"更新配置失败: {e}")
            return False


# 创建一个全局配置实例供其他模块使用
config = Config()

owner_id = config.owner_id
ws_url = config.ws_url
token = config.token
DD_BOT_TOKEN = config.DD_BOT_TOKEN
DD_BOT_SECRET = config.DD_BOT_SECRET
