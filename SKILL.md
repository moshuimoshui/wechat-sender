---
name: 微信发送消息
description: 通过微信桌面版自动发送消息或文件给指定联系人或群聊。支持文字和文件两种模式。依赖 uiautomation 库和微信PC版（Weixin）。
---

# 微信发送消息

通过微信桌面版自动发送消息或文件给指定联系人或群聊。

## 依赖
- 微信PC版已登录
- Python uiautomation 库（`pip install uiautomation`）

## 用法

```bash
# 发送文字
python wechat_sender.py "收件人" "消息内容"

# 发送文件
python wechat_sender.py "收件人" "文件路径" --mode file

# Ctrl+Enter换行模式（输入但不发送）
python wechat_sender.py "收件人" "多行内容" --no-send
```

## 触发关键词
微信发送、发微信、发给、wechat send

## WorkBuddy 安装

将此仓库克隆到 `~/.workbuddy/skills/微信发送消息/` 即可使用。
