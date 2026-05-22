# 微信发送消息 Skill · WeChat Sender

[![Agent Ready](https://img.shields.io/badge/AI_Agent-✅_Ready-brightgreen)](https://github.com/moshuimoshui/wechat-sender)
[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)
[![License MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

通过 Python UIA (UI Automation) 自动操作微信 PC 版，发送消息或文件给指定联系人或群聊。可作为独立脚本使用，也可接入 AI Agent。

## 原理

使用微软官方 UIA (UI Automation) 接口直接操控微信窗口，不需要 AHK 或其他第三方工具。相比传统的模拟按键，UIA 更底层、更可靠。

## 依赖

- Windows 系统
- 微信 PC 版（Weixin）已登录
- Python 3.x + `uiautomation` 库

```bash
pip install uiautomation
```

## 用法

```bash
# 发送文字消息
python wechat_sender.py "收件人" "消息内容"

# 发送文件
python wechat_sender.py "收件人" "文件路径" --mode file

# 输入多行文本但不发送（Ctrl+Enter 换行）
python wechat_sender.py "收件人" "多行\n内容" --no-send
```

## 参数

| 参数 | 说明 |
|------|------|
| `收件人` | 微信联系人或群聊名称（必填） |
| `内容` | 文字消息或文件路径 |
| `--mode file` | 文件模式，将文件复制到剪贴板后粘贴发送 |
| `--no-send` | 仅输入到文本框，不发送 |

## 工作流程

1. 自动查找正在运行的微信窗口（类名 `mmui::MainWindow`）
2. 未运行则自动启动微信
3. 多重 API 激活窗口到前台
4. 搜索联系人/群聊
5. 输入内容并发送

## 注意事项

- 微信会阻止 `WinActivate` 等传统窗口激活方式，脚本使用了 `ShowWindow` + `SwitchToThisWindow` + `SetForegroundWindow` + `SetFocus` 等 5 种方式组合激活
- 搜索联系人后需按 ↑ 键选中结果（微信新版搜索逻辑）
- 多行文本使用 `Ctrl+Enter` 换行（对应微信的换行而非发送）

## 许可证

MIT
