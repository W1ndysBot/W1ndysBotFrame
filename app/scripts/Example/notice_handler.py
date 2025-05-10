# app/scripts/Example/notice_handler.py

import logging
from app.api.message import send_group_msg
from app.scripts.Example.data_manager import DataManager


class NoticeHandler:
    """通知处理器

    负责处理:
    - 群成员变动
    - 群管理员变动
    - 群荣誉变动
    - 群禁言
    - 好友添加
    等通知事件
    """

    def __init__(self):
        """初始化通知处理器

        Args:
            data_manager: DataManager实例，用于管理数据和开关状态
        """
        try:
            # 初始化 DataManager 实例
            self.data_manager = DataManager()
            # 保存websocket连接
            self.websocket = None
            self.notice_type = ""
            self.group_id = ""
            self.user_id = ""
            self.operator_id = ""
            self.message_id = ""
            self.sub_type = ""
            self.duration = 0
            self.card_new = ""
            self.card_old = ""
            self.sender_id = ""
            self.target_id = ""
            self.title = ""
            self.file_info = {}
        except Exception as e:
            logging.error(f"[Example]初始化通知处理器失败: {e}")
            raise

    async def handle(self, msg):
        """处理所有通知类型

        根据 NapCatQQ 的上报事件类型，通知事件可以分为多种类型:
        - notice.friend_add: 好友添加
        - notice.friend_recall: 私聊消息撤回
        - notice.group_admin: 群管理员变动
        - notice.group_ban: 群禁言
        - notice.group_card: 群成员名片更新
        - notice.group_decrease: 群成员减少
        - notice.group_increase: 群成员增加
        - notice.group_recall: 群消息撤回
        - notice.group_upload: 群文件上传
        - notice.essence: 群精华消息
        - notice.notify: 各种提醒类通知
        """
        try:
            self.notice_type = msg.get("notice_type", "")
            self.group_id = msg.get("group_id", "")

            # 检查群相关通知的功能是否开启
            if (
                self.group_id
                and self.notice_type.startswith("group_")
                and not self.data_manager.load_function_status(self.group_id)
            ):
                return

            # 根据通知类型分发处理
            if self.notice_type == "friend_add":
                await self.handle_friend_add(msg)
            elif self.notice_type == "friend_recall":
                await self.handle_friend_recall(msg)
            elif self.notice_type == "group_admin":
                await self.handle_group_admin(msg)
            elif self.notice_type == "group_ban":
                await self.handle_group_ban(msg)
            elif self.notice_type == "group_card":
                await self.handle_group_card(msg)
            elif self.notice_type == "group_decrease":
                await self.handle_group_decrease(msg)
            elif self.notice_type == "group_increase":
                await self.handle_group_increase(msg)
            elif self.notice_type == "group_recall":
                await self.handle_group_recall(msg)
            elif self.notice_type == "group_upload":
                await self.handle_group_upload(msg)
            elif self.notice_type == "essence":
                await self.handle_essence(msg)
            elif self.notice_type == "notify":
                await self.handle_notify(msg)
        except Exception as e:
            logging.error(f"[Example]分发处理通知事件失败: {e}")
            if self.group_id:
                try:
                    await send_group_msg(
                        self.websocket,
                        self.group_id,
                        f"分发处理通知事件失败，错误信息：{str(e)}",
                    )
                except Exception as inner_e:
                    logging.error(f"[Example]发送错误通知失败: {inner_e}")
            return

    async def handle_friend_add(self, msg):
        """处理好友添加事件

        字段列表:
        - user_id: 新添加好友 QQ 号
        """
        try:
            self.user_id = str(msg.get("user_id", ""))
            # 处理好友添加逻辑

        except Exception as e:
            logging.error(f"[Example]处理好友添加事件失败: {e}")

    async def handle_friend_recall(self, msg):
        """处理私聊消息撤回事件

        字段列表:
        - user_id: 好友 QQ 号
        - message_id: 被撤回的消息 ID
        """
        try:
            self.user_id = str(msg.get("user_id", ""))
            self.message_id = msg.get("message_id", "")
            # 处理私聊撤回逻辑

        except Exception as e:
            logging.error(f"[Example]处理私聊撤回事件失败: {e}")

    async def handle_group_increase(self, msg):
        """处理群成员增加事件

        字段列表:
        - sub_type: 子类型，approve/invite
        - group_id: 群号
        - operator_id: 操作者 QQ 号
        - user_id: 加入者 QQ 号
        """
        try:
            self.group_id = msg.get("group_id", "")
            self.user_id = str(msg.get("user_id", ""))
            self.operator_id = msg.get("operator_id", "")
            self.sub_type = msg.get("sub_type", "")

            # 根据子类型处理不同情况
            if self.sub_type == "approve":
                # 管理员已同意入群
                pass
            elif self.sub_type == "invite":
                # 管理员邀请入群
                pass

        except Exception as e:
            logging.error(f"[Example]处理群成员增加事件失败: {e}")
            if self.group_id:
                await send_group_msg(
                    self.websocket,
                    self.group_id,
                    f"处理群成员增加事件失败，错误信息：{str(e)}",
                )

    async def handle_group_decrease(self, msg):
        """处理群成员减少事件

        字段列表:
        - sub_type: 子类型，leave/kick/kick_me
        - group_id: 群号
        - operator_id: 操作者 QQ 号 (如果是主动退群，则和 user_id 相同)
        - user_id: 离开者 QQ 号
        """
        try:
            self.group_id = msg.get("group_id", "")
            self.user_id = str(msg.get("user_id", ""))
            self.operator_id = msg.get("operator_id", "")
            self.sub_type = msg.get("sub_type", "")

            # 根据子类型处理不同情况
            if self.sub_type == "leave":
                # 主动退群
                pass
            elif self.sub_type == "kick":
                # 成员被踢
                pass
            elif self.sub_type == "kick_me":
                # 登录号被踢
                pass

        except Exception as e:
            logging.error(f"[Example]处理群成员减少事件失败: {e}")
            if self.group_id:
                await send_group_msg(
                    self.websocket,
                    self.group_id,
                    f"处理群成员减少事件失败，错误信息：{str(e)}",
                )

    async def handle_group_admin(self, msg):
        """处理群管理员变动事件

        字段列表:
        - sub_type: 子类型，set/unset
        - group_id: 群号
        - user_id: 管理员变动目标 QQ 号
        """
        try:
            self.group_id = msg.get("group_id", "")
            self.user_id = str(msg.get("user_id", ""))
            self.sub_type = msg.get("sub_type", "")

            # 根据子类型处理不同情况
            if self.sub_type == "set":
                # 设置管理员
                pass
            elif self.sub_type == "unset":
                # 取消管理员
                pass

        except Exception as e:
            logging.error(f"[Example]处理群管理员变动事件失败: {e}")
            if self.group_id:
                await send_group_msg(
                    self.websocket,
                    self.group_id,
                    f"处理群管理员变动事件失败，错误信息：{str(e)}",
                )

    async def handle_group_ban(self, msg):
        """处理群禁言事件

        字段列表:
        - sub_type: 子类型，ban/lift_ban
        - group_id: 群号
        - operator_id: 操作者 QQ 号
        - user_id: 被禁言 QQ 号
        - duration: 禁言时长，单位秒
        """
        try:
            self.group_id = msg.get("group_id", "")
            self.user_id = str(msg.get("user_id", ""))
            self.operator_id = msg.get("operator_id", "")
            self.sub_type = msg.get("sub_type", "")
            self.duration = msg.get("duration", 0)

            # 根据子类型处理不同情况
            if self.sub_type == "ban":
                # 禁言
                pass
            elif self.sub_type == "lift_ban":
                # 解除禁言
                pass

        except Exception as e:
            logging.error(f"[Example]处理群禁言事件失败: {e}")
            if self.group_id:
                await send_group_msg(
                    self.websocket,
                    self.group_id,
                    f"处理群禁言事件失败，错误信息：{str(e)}",
                )

    async def handle_group_card(self, msg):
        """处理群成员名片更新事件

        字段列表:
        - group_id: 群号
        - user_id: 成员 QQ 号
        - card_new: 新名片
        - card_old: 旧名片
        """
        try:
            self.group_id = msg.get("group_id", "")
            self.user_id = str(msg.get("user_id", ""))
            self.card_new = msg.get("card_new", "")
            self.card_old = msg.get("card_old", "")

            # 处理名片更新逻辑

        except Exception as e:
            logging.error(f"[Example]处理群成员名片更新事件失败: {e}")

    async def handle_group_recall(self, msg):
        """处理群消息撤回事件

        字段列表:
        - group_id: 群号
        - user_id: 消息发送者 QQ 号
        - operator_id: 操作者 QQ 号
        - message_id: 被撤回的消息 ID
        """
        try:
            self.group_id = msg.get("group_id", "")
            self.user_id = str(msg.get("user_id", ""))
            self.operator_id = msg.get("operator_id", "")
            self.message_id = msg.get("message_id", "")

            # 处理群消息撤回逻辑

        except Exception as e:
            logging.error(f"[Example]处理群消息撤回事件失败: {e}")

    async def handle_group_upload(self, msg):
        """处理群文件上传事件

        字段列表:
        - group_id: 群号
        - user_id: 上传者 QQ 号
        - file: 文件信息
        """
        try:
            self.group_id = msg.get("group_id", "")
            self.user_id = str(msg.get("user_id", ""))
            self.file_info = msg.get("file", {})

            # 处理群文件上传逻辑

        except Exception as e:
            logging.error(f"[Example]处理群文件上传事件失败: {e}")

    async def handle_essence(self, msg):
        """处理精华消息事件

        字段列表:
        - sub_type: 子类型，add
        - group_id: 群号
        - sender_id: 消息发送者 QQ 号
        - operator_id: 操作者 QQ 号
        - message_id: 消息 ID
        """
        try:
            self.group_id = msg.get("group_id", "")
            self.sender_id = msg.get("sender_id", "")
            self.operator_id = msg.get("operator_id", "")
            self.message_id = msg.get("message_id", "")
            self.sub_type = msg.get("sub_type", "")

            # 根据子类型处理不同情况
            if self.sub_type == "add":
                # 添加精华消息
                pass

        except Exception as e:
            logging.error(f"[Example]处理精华消息事件失败: {e}")

    async def handle_notify(self, msg):
        """处理提醒类通知

        可能的子类型:
        - poke: 戳一戳
        - input_status: 输入状态更新
        - title: 群成员头衔变更
        - profile_like: 点赞

        字段因子类型而异
        """
        try:
            self.sub_type = msg.get("sub_type", "")

            # 根据子类型处理不同情况
            if self.sub_type == "poke":
                # 处理戳一戳
                self.group_id = msg.get("group_id", "")
                self.user_id = str(msg.get("user_id", ""))
                self.target_id = msg.get("target_id", "")

            elif self.sub_type == "input_status":
                # 处理输入状态更新
                self.user_id = str(msg.get("user_id", ""))

            elif self.sub_type == "title":
                # 处理群成员头衔变更
                self.group_id = msg.get("group_id", "")
                self.user_id = str(msg.get("user_id", ""))
                self.title = msg.get("title", "")

            elif self.sub_type == "profile_like":
                # 处理点赞
                self.user_id = str(msg.get("user_id", ""))

        except Exception as e:
            logging.error(f"[Example]处理通知事件失败: {e}")
