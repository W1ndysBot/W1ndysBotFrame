# 🤖 W1ndysBot

这是 https://github.com/W1ndys/W1ndysBot 的运行框架，基于 NapCat 和 Python 开发。

## 📁 项目结构

```

W1ndysBot/
├── app/                    # 主应用目录
│   ├── data/              # 数据存储目录
│   │   ├── GroupSwitch/   # 群组开关数据
│   │   └── Example/       # 示例功能数据
│   ├── logs/              # 日志文件目录
│   ├── scripts/           # 功能模块目录
│   │   └── Example/       # 示例功能模块
│   │       ├── main.py    # 功能模块主文件
│   │       └── README.md  # 功能模块说明
│   ├── api.py            # API 接口封装
│   ├── bot.py            # 机器人核心
│   ├── config.py         # 配置文件
│   ├── dingtalk.py       # 钉钉通知
│   ├── handler_events.py # 事件处理器
│   ├── logger.py         # 日志配置
│   ├── main.py           # 程序入口
│   ├── switch.py         # 群组开关管理
│   └── system.py         # 系统功能
└── README.md             # 项目说明

```

## ✨ 功能说明

- 🔄 群组开关管理：每个群可以单独控制功能的开启/关闭
- 📝 日志系统：支持日志记录和查询
- 💬 钉钉通知：支持发送通知到钉钉
- 🔌 模块化设计：功能模块可以独立开发和管理

## 🛠️ 开发说明

- 新功能开发请参考 `app/scripts/Example` 目录的示例
- 每个功能模块需要包含:
  - `main.py`: 功能实现
  - `README.md`: 功能说明
- 数据存储请在 `app/data` 下创建对应目录

## ⚙️ 配置说明

在 `app/config.py` 中配置:

- `owner_id`: 机器人管理员 QQ 号
- `ws_url`: WebSocket 连接地址
- `token`: 认证 token(可选)

## 📜 脚本说明

### 环境配置脚本

- `create_venv_windows.bat`: Windows 下创建 Python 虚拟环境
- `create_venv_linux.sh`: Linux 下创建 Python 虚拟环境
- `open_venv_terminal_windows.bat`: Windows 下打开虚拟环境终端

### 运行脚本

- `run_app.sh`: Linux 下后台运行机器人
- `run_app_in_venv_windows.bat`: Windows 下在虚拟环境中运行机器人
- `restart_app.sh`: Linux 下重启机器人

### Git 管理脚本

- `git_init_submodules.sh`: 初始化所有子模块
- `git_add_submodule.sh`: 添加新的子模块
- `git_remove_submodule.sh`: 删除指定子模块
- `git_reinstall_submodule.sh`: 重新安装指定子模块
- `git_update_all.sh`: 更新主仓库和所有子模块
- `git_update_repo.sh`: 更新主仓库
- `git_update_submodules.sh`: 更新子模块

### NapCat Docker 相关脚本

- `run_napcat_docker_win.bat`: Windows 下运行 NapCat Docker
- `linux_run_napcat_docker.sh`: Linux 下运行 NapCat Docker
- `linux_update_napcat.sh`: Linux 下更新 NapCat Docker
