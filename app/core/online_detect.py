# app/core/online_detect.py

import logging
import config
from api.message import send_private_msg
from core.feishu import feishu
from core.dingtalk import dingtalk
import time
import asyncio


class OnlineDetectManager:
    def __init__(self):
        self.is_online = True  # 初始状态为在线
        self.last_state_change_time = 0
        self.last_report_time = 0
        # 状态变化的最小时间间隔(秒)，防止频繁上报
        self.min_report_interval = 60
        self.owner_id = config.owner_id

    async def handle_events(self, websocket, message):
        """处理心跳事件，检测在线状态"""
        # 处理首次连接事件
        if (
            message.get("post_type") == "meta_event"
            and message.get("meta_event_type") == "lifecycle"
            and message.get("sub_type") == "connect"
        ):
            current_time = time.strftime(
                "%Y-%m-%d %H:%M:%S",
                time.localtime(message.get("time", int(time.time()))),
            )
            connect_msg = f"W1ndysGroupBot已上线！\n机器人ID: {message.get('self_id')}\n上线时间: {current_time}"
            logging.info(f"机器人首次连接: {connect_msg}")

            # 向所有管理员发送私聊消息
            try:
                tasks = [
                    send_private_msg(websocket, owner, connect_msg)
                    for owner in self.owner_id
                ]
                await asyncio.gather(*tasks)
            except Exception as e:
                logging.error(f"发送上线通知失败: {e}")
            return

        # 只处理心跳事件
        if (
            message.get("post_type") != "meta_event"
            or message.get("meta_event_type") != "heartbeat"
        ):
            return

        # 获取在线状态
        status = message.get("status", {})
        current_online = status.get("online", False)

        # 如果是首次检测或状态发生变化
        current_time = int(time.time())
        if self.is_online is None or self.is_online != current_online:
            # 检查是否达到最小上报间隔
            if current_time - self.last_report_time >= self.min_report_interval:
                self.last_state_change_time = current_time
                self.last_report_time = current_time

                # 生成通知消息
                if self.is_online is None:
                    status_text = "初始化" if current_online else "掉线"
                else:
                    status_text = "重新上线" if current_online else "掉线"

                title = f"机器人状态变更: {status_text}"
                content = (
                    f"机器人ID: {message.get('self_id')}\n"
                    f"当前状态: {'在线' if current_online else '离线'}\n"
                    f"状态变更时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))}\n"
                    f"心跳间隔: {message.get('interval', 0)/1000}秒"
                )

                # 发送通知
                logging.info(f"机器人状态变更: {status_text}")
                try:
                    # 发送飞书通知
                    feishu_result = feishu(title, content)
                    if "error" in feishu_result:
                        logging.error(f"发送飞书通知失败: {feishu_result.get('error')}")

                    # 发送钉钉通知
                    dingtalk(title, content)
                except Exception as e:
                    logging.error(f"发送通知失败: {e}")

            # 更新状态
            self.is_online = current_online


# 创建全局实例
Online_detect_manager = OnlineDetectManager()
