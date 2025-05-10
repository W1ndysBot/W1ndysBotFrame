# logger.py

import logging
import colorlog
import os
from datetime import datetime, timezone, timedelta
from logging.handlers import RotatingFileHandler


class Logger:
    def __init__(self):
        self.logs_dir = None
        self.log_filename = None
        self.root_logger = logging.getLogger()

    def setup(self):
        """设置日志器"""
        # 清除之前的处理器
        self.root_logger.handlers = []

        handler = colorlog.StreamHandler()
        handler.setFormatter(
            colorlog.ColoredFormatter(
                "%(log_color)s%(asctime)s %(levelname)s:%(name)s:[%(filename)s:%(lineno)d:%(funcName)s:%(module)s:%(threadName)s]\n%(message)s\n",  # 添加日期和换行符
                datefmt="%Y-%m-%d %H:%M:%S",  # 日期格式
                log_colors={
                    "DEBUG": "cyan",
                    "INFO": "light_green",  # 使用更亮的绿色
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "red,bg_white",
                },
            )
        )

        # 获取当前脚本所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.logs_dir = os.path.join(current_dir, "logs")

        # 创建 logs 目录
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)

        # 以当前启动时间为文件名，使用东八区时间
        tz = timezone(timedelta(hours=8))
        self.log_filename = os.path.join(
            self.logs_dir, datetime.now(tz).strftime("%Y-%m-%d_%H-%M-%S.log")
        )

        # 添加 RotatingFileHandler 将日志保存到本地文件，并在超过1MB时新建文件
        file_handler = RotatingFileHandler(
            self.log_filename, maxBytes=1024 * 1024, backupCount=0, encoding="utf-8"
        )
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s:%(name)s:[%(filename)s:%(funcName)s:%(lineno)d:%(module)s:%(threadName)s]\n%(message)s\n",  # 添加日期和换行符
                datefmt="%Y-%m-%d %H:%M:%S",  # 日期格式
            )
        )
        file_handler.namer = lambda name: name.replace(
            ".log", f"_{datetime.now(tz).strftime('%Y-%m-%d_%H-%M-%S')}.log"
        )
        file_handler.rotator = lambda source, dest: os.rename(source, dest)

        # 设置根日志记录器的级别和处理器
        self.root_logger.setLevel(logging.INFO)
        handler.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        self.root_logger.addHandler(handler)
        self.root_logger.addHandler(file_handler)

        # 确保日志及时刷新
        for handler in self.root_logger.handlers:
            handler.flush()

        logging.info("初始化日志器")
        logging.info(f"日志文件名: {self.log_filename}")

        return self.log_filename


# 创建一个全局日志器实例
logger = Logger()
