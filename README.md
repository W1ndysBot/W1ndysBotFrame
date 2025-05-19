# 🤖 W1ndysBotFrame

## 项目正在重构阶段，可能不稳定！！！

W1ndysBotFrame，一款基于 NapCat 和 Python 开发的机器人程序。

本仓库可能更新不及时，如有需要，请参考 https://github.com/W1ndys/W1ndysBot 的最新更新

## 📁 项目结构

```
app/
├── api/                    # API 接口模块
│   ├── user.py            # 用户相关接口
│   ├── message.py         # 消息处理接口
│   ├── generate.py        # 生成相关接口
│   └── group.py           # 群组管理接口
├── core/                   # 核心功能模块
│   ├── feishu.py          # 飞书集成
│   └── online_detect.py   # 在线检测
├── modules/               # 模块目录
│   └── Example/          # 示例模块
│       ├── main.py              # 主程序入口
│       ├── handle_message.py   # 消息处理器
│       ├── handle_notice.py    # 通知处理器
│       ├── handle_request.py   # 请求处理器
│       ├── handle_response.py  # 响应处理器
│       └── README.md           # 说明文档
├── bot.py                 # 机器人主程序
├── handle_events.py      # 事件处理器
├── main.py               # 程序入口
├── logger.py             # 日志系统
└── config.py             # 配置文件
```

## 流程图

在这里->[流程图](./docs/flow_diagram.md)

## ✨ 功能说明

- 🔄 在线检测：检测机器人是否在线
- 🔄 群组开关管理：每个群可以单独控制功能的开启/关闭
- 🔄 私聊功能开关管理：每个私聊功能可以单独控制功能的开启/关闭
- 🔄 定时任务：支持定时任务
- 🔄 私聊转达：支持私聊转达到`OWNER`管理员
- 📝 日志系统：支持日志记录和查询
- 💬 飞书通知：支持掉线后自动发送通知到飞书
- 🔌 模块化设计：功能模块可以独立开发和管理

## 🛠️ 开发说明

- 新功能开发请参考 `app/modules/example` 目录的示例
- 数据存储请在 `app/data` 下创建对应目录

## ⚙️ 配置说明

在 `app/config.py` 中配置:

- `OWNER_ID`: 机器人管理员 QQ 号
- `WS_URL`: WebSocket 连接地址
- `TOKEN`: 认证 token(可选)
- `FEISHU_BOT_URL`: 飞书机器人 URL(可选)
- `FEISHU_BOT_SECRET`: 飞书机器人 Secret(可选)
