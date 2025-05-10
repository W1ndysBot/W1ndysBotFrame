#!/bin/bash

# 切换到项目根目录
cd "$(dirname "$0")"

# 添加./app/data目录下的所有改动文件
git add ./app/data

# 提交改动，提交信息为"备份数据"
git commit -m "chore(data): 备份数据"

echo "数据备份已提交到Git仓库"

# # 推送到远程仓库
git push origin main

echo "数据备份已推送到远程仓库"
