# main.py


import os
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from logger import logger
from bot import connect_to_bot

# 加载.env文件中的环境变量
load_dotenv()


def verify_environment_variables():
    """验证环境变量是否正确加载"""

    # 验证飞书机器人凭证
    if not os.environ.get("FEISHU_BOT_URL") or not os.environ.get("FEISHU_BOT_SECRET"):
        logger.warning(
            "警告: 未设置飞书机器人凭证（FEISHU_BOT_URL和FEISHU_BOT_SECRET），飞书机器人可能无法正常工作"
        )
    else:
        logger.info("飞书机器人凭证已设置")


class Application:
    def __init__(self):

        # 验证环境变量
        verify_environment_variables()

    async def run(self):
        """运行主程序"""
        # 打印当前运行根目录
        logger.info(f"当前运行根目录: {os.getcwd()}")
        while True:
            try:
                result = await connect_to_bot()
                if result is None:
                    raise ValueError("连接返回None")
            except Exception as e:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.error(f"连接失败，正在重试: {e} 当前时间: {current_time}")

                await asyncio.sleep(2)  # 每2秒重试一次


if __name__ == "__main__":

    app = Application()
    asyncio.run(app.run())
