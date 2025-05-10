# main.py

import sys
import os
import asyncio
import logging
from datetime import datetime
from dotenv import load_dotenv

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logger import logger
from bot import bot

# 加载.env文件中的环境变量
load_dotenv()


def verify_environment_variables():
    """验证环境变量是否正确加载"""
    # 验证阿里云API凭证
    if not os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID") or not os.environ.get(
        "ALIBABA_CLOUD_ACCESS_KEY_SECRET"
    ):
        logging.warning(
            "警告: 未设置阿里云API凭证，阿里云内容安全检测服务可能无法正常工作"
        )
    else:
        logging.info("阿里云API凭证已设置")

    # 验证飞书机器人凭证
    if not os.environ.get("FEISHU_BOT_URL") or not os.environ.get("FEISHU_BOT_SECRET"):
        logging.warning("警告: 未设置飞书机器人凭证，飞书机器人可能无法正常工作")
    else:
        logging.info("飞书机器人凭证已设置")

    # 验证钉钉机器人凭证
    if not os.environ.get("DD_BOT_URL") or not os.environ.get("DD_BOT_SECRET"):
        logging.warning("警告: 未设置钉钉机器人凭证，钉钉机器人可能无法正常工作")
    else:
        logging.info("钉钉机器人凭证已设置")


class Application:
    def __init__(self):
        # 初始化日志
        logger.setup()
        # 验证环境变量
        verify_environment_variables()

    async def run(self):
        """运行主程序"""
        while True:
            try:
                result = await bot.connect()
                if result is None:
                    raise ValueError("连接返回None")
            except Exception as e:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logging.error(f"连接失败，正在重试: {e} 当前时间: {current_time}")

                await asyncio.sleep(1)  # 每秒重试一次


if __name__ == "__main__":

    app = Application()
    asyncio.run(app.run())
