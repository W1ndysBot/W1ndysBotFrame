@echo off
chcp 65001

:: 激活Python虚拟环境
call venv\Scripts\activate

:: 进入app目录
cd app

:: 运行主程序
python main.py

:: 如果程序意外退出，暂停以便查看错误信息
pause 