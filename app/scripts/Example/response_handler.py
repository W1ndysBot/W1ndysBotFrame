# app/scripts/Example/response_handler.py

import logging
from app.api.message import send_group_msg, send_private_msg
from app.scripts.Example.data_manager import DataManager


class ResponseHandler:
    """响应处理器

    负责处理:
    - API回调响应
    - 异步操作结果处理
    - 定时任务响应
    """

    def __init__(self):
        """初始化响应处理器

        Args:
            data_manager: DataManager实例，用于管理数据和状态
        """
        try:
            # 初始化 DataManager 实例
            self.data_manager = DataManager()
            # 保存websocket连接
            self.websocket = None
            self.status = ""
            self.retcode = -1
            self.data = {}
            self.echo = ""
        except Exception as e:
            logging.error(f"[Example]初始化响应处理器失败: {e}")
            raise

    async def handle(self, msg):
        """处理所有回调响应

        回调响应是指 API 调用后服务器返回的结果，包括:
        - status: 通常为 "ok" 表示成功
        - retcode: 返回码，0 表示成功，其他值表示失败
        - data: 返回的数据
        - echo: 回传的请求标识，用于区分不同的请求
        """
        try:
            self.echo = msg.get("echo", "")

            # 检查消息是否包含有效的echo字段
            if not self.echo:
                return

            # 根据echo内容分发到不同的处理方法
            if self.echo.startswith("example_group_"):
                await self.handle_group_operation_response(msg)
            elif self.echo.startswith("example_private_"):
                await self.handle_private_operation_response(msg)
            elif self.echo.startswith("example_request_"):
                await self.handle_request_operation_response(msg)
            elif self.echo.startswith("example_notice_"):
                await self.handle_notice_operation_response(msg)
            elif self.echo.startswith("example_scheduled_"):
                await self.handle_scheduled_task_response(msg)

        except Exception as e:
            logging.error(f"[Example]处理Example回调事件失败: {e}")
            group_id = msg.get("group_id", "")
            user_id = str(msg.get("user_id", ""))

            if group_id:
                await send_group_msg(
                    self.websocket,
                    group_id,
                    f"处理Example回调事件失败，错误信息：{str(e)}",
                )
            elif user_id:
                await send_private_msg(
                    self.websocket,
                    user_id,
                    f"处理Example回调事件失败，错误信息：{str(e)}",
                )
            return

    async def handle_group_operation_response(self, msg):
        """处理群操作的响应结果

        字段列表:
        - status: 状态，通常为 "ok"
        - retcode: 返回码，0 表示成功
        - data: 返回的数据
        - echo: 回传的请求标识
        """
        try:
            self.echo = msg.get("echo", "")
            self.status = msg.get("status", "")
            self.retcode = msg.get("retcode", -1)
            self.data = msg.get("data", {})

            # 从echo中提取必要信息
            # 示例: example_group_send_123456_987654321
            # 其中123456为群号，987654321为操作ID
            parts = self.echo.split("_")
            if len(parts) >= 4:
                operation = parts[2]  # 操作类型，如send, kick等
                group_id = parts[3]  # 群号
                op_id = parts[4] if len(parts) > 4 else ""  # 操作ID

                # 根据操作类型和结果进行处理
                if operation == "send":
                    await self._handle_send_message_response(
                        self.status, self.retcode, group_id, op_id, self.data
                    )
                elif operation == "kick":
                    await self._handle_kick_member_response(
                        self.status, self.retcode, group_id, op_id
                    )
                # 可以添加更多操作类型

        except Exception as e:
            logging.error(f"[Example]处理群操作响应失败: {e}")

    async def handle_private_operation_response(self, msg):
        """处理私聊操作的响应结果

        字段列表:
        - status: 状态，通常为 "ok"
        - retcode: 返回码，0 表示成功
        - data: 返回的数据
        - echo: 回传的请求标识
        """
        try:
            self.echo = msg.get("echo", "")
            self.status = msg.get("status", "")
            self.retcode = msg.get("retcode", -1)
            self.data = msg.get("data", {})

            # 处理私聊相关的响应
            # 从echo中提取信息并处理
            parts = self.echo.split("_")
            if len(parts) >= 4:
                operation = parts[2]  # 操作类型
                user_id = parts[3]  # 用户QQ号

                # 根据操作类型处理
                if operation == "send":
                    # 处理私聊消息发送响应
                    pass

        except Exception as e:
            logging.error(f"[Example]处理私聊操作响应失败: {e}")

    async def handle_request_operation_response(self, msg):
        """处理请求操作(如加好友、加群)的响应结果

        字段列表:
        - status: 状态，通常为 "ok"
        - retcode: 返回码，0 表示成功
        - data: 返回的数据
        - echo: 回传的请求标识
        """
        try:
            self.echo = msg.get("echo", "")
            self.status = msg.get("status", "")
            self.retcode = msg.get("retcode", -1)
            self.data = msg.get("data", {})

            # 处理请求相关的响应
            parts = self.echo.split("_")
            if len(parts) >= 4:
                operation = parts[2]  # 操作类型
                request_type = parts[3]  # 请求类型

                # 根据操作类型和请求类型处理
                if operation == "approve" and request_type == "friend":
                    # 处理好友请求通过响应
                    pass
                elif operation == "approve" and request_type == "group":
                    # 处理群请求通过响应
                    pass

        except Exception as e:
            logging.error(f"[Example]处理请求操作响应失败: {e}")

    async def handle_notice_operation_response(self, msg):
        """处理通知操作的响应结果

        字段列表:
        - status: 状态，通常为 "ok"
        - retcode: 返回码，0 表示成功
        - data: 返回的数据
        - echo: 回传的请求标识
        """
        try:
            self.echo = msg.get("echo", "")
            self.status = msg.get("status", "")
            self.retcode = msg.get("retcode", -1)
            self.data = msg.get("data", {})

            # 处理通知相关的响应
            parts = self.echo.split("_")
            if len(parts) >= 4:
                operation = parts[2]  # 操作类型
                notice_type = parts[3]  # 通知类型

                # 根据操作类型和通知类型处理
                if operation == "set" and notice_type == "group_card":
                    # 处理设置群名片响应
                    pass

        except Exception as e:
            logging.error(f"[Example]处理通知操作响应失败: {e}")

    async def handle_scheduled_task_response(self, msg):
        """处理定时任务的响应结果

        字段列表:
        - status: 状态，通常为 "ok"
        - retcode: 返回码，0 表示成功
        - data: 返回的数据
        - echo: 回传的请求标识
        """
        try:
            self.echo = msg.get("echo", "")
            self.status = msg.get("status", "")
            self.retcode = msg.get("retcode", -1)
            self.data = msg.get("data", {})

            # 处理定时任务相关的响应
            parts = self.echo.split("_")
            if len(parts) >= 4:
                task_type = parts[2]  # 任务类型
                task_id = parts[3]  # 任务ID

                # 根据任务类型处理
                if task_type == "daily":
                    # 处理每日任务响应
                    pass
                elif task_type == "weekly":
                    # 处理每周任务响应
                    pass

        except Exception as e:
            logging.error(f"[Example]处理定时任务响应失败: {e}")

    async def _handle_send_message_response(
        self, status, retcode, group_id, op_id, data=None
    ):
        """处理发送消息操作的响应"""
        if status == "ok" and retcode == 0:
            # 获取成功发送的消息ID
            message_id = data.get("message_id", "") if data else ""
            logging.info(
                f"群 {group_id} 消息发送成功，操作ID: {op_id}, 消息ID: {message_id}"
            )
        else:
            logging.error(
                f"群 {group_id} 消息发送失败，操作ID: {op_id}, 状态: {status}, 错误码: {retcode}"
            )
            # 可以根据需要实现重试逻辑或其他错误处理

    async def _handle_kick_member_response(self, status, retcode, group_id, op_id):
        """处理踢出成员操作的响应"""
        if status == "ok" and retcode == 0:
            logging.info(f"群 {group_id} 踢出成员成功，操作ID: {op_id}")
        else:
            logging.error(
                f"群 {group_id} 踢出成员失败，操作ID: {op_id}, 状态: {status}, 错误码: {retcode}"
            )
            # 可以根据需要通知群管理员
