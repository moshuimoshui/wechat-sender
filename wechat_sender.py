# -*- coding: utf-8 -*-
"""
微信桌面版自动发送消息/文件
用法:
  # 文字消息
  python send_wechat.py "收件人" "消息内容"
  python send_wechat.py "收件人" "多行\n内容" --no-send

  # 单个文件
  python send_wechat.py "收件人" "文件路径" --mode file

  # 多个文件（一次性粘贴发送，只搜索一次联系人）
  python send_wechat.py "收件人" "文件1" "文件2" "文件3" --mode file

注意：
- uiautomation SendKeys 对某些 emoji 编码支持不佳，可能导致乱码
- 多行内容中的空行已被脚本自动跳过处理，不会报错
- 多个文件通过 PowerShell Set-Clipboard 一次性复制到剪贴板，微信支持批量粘贴
"""
import uiautomation as auto
import subprocess
import time
import ctypes
import sys
import os

# ===== 配置 =====
WECHAT_PATH = r'C:\Program Files\Tencent\Weixin\Weixin.exe'

def ctrl_enter():
    """Ctrl+Enter 换行（非发送）"""
    ctypes.windll.user32.keybd_event(0x11, 0, 0, 0)
    ctypes.windll.user32.keybd_event(0x0D, 0, 0, 0)
    ctypes.windll.user32.keybd_event(0x0D, 0, 2, 0)
    ctypes.windll.user32.keybd_event(0x11, 0, 2, 0)

def find_wechat():
    """查找微信主窗口（mmui::MainWindow 类名）"""
    for w in auto.GetRootControl().GetChildren():
        try:
            if w.ClassName == 'mmui::MainWindow':
                return w
        except:
            pass
    return None

def activate_window(wechat):
    """多重API激活微信窗口"""
    hwnd = wechat.NativeWindowHandle
    ctypes.windll.user32.ShowWindow(hwnd, 9)
    time.sleep(0.2)
    ctypes.windll.user32.SwitchToThisWindow(hwnd, True)
    time.sleep(0.3)
    ctypes.windll.user32.SetForegroundWindow(hwnd)
    time.sleep(0.3)
    ctypes.windll.user32.BringWindowToTop(hwnd)
    time.sleep(0.3)
    wechat.SetFocus()
    time.sleep(1)

def search_and_open(wechat, recipient):
    """在微信中搜索并打开联系人或群聊"""
    wechat.SendKeys('{Ctrl}f')
    time.sleep(0.5)
    wechat.SendKeys(recipient)
    time.sleep(1.5)
    wechat.SendKeys('{Up}')  # 选中搜索结果
    time.sleep(0.5)
    wechat.SendKeys('{Enter}')
    time.sleep(1.5)

def send_text(wechat, text, no_send=False):
    """发送文字（支持多行）"""
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if line == '':
            # 空行：直接 Ctrl+Enter 换行
            ctrl_enter()
            time.sleep(0.2)
            continue
        wechat.SendKeys(line)
        time.sleep(0.1)
        if i < len(lines) - 1:
            ctrl_enter()  # Ctrl+Enter 换行
            time.sleep(0.2)
    
    if not no_send:
        time.sleep(0.3)
        wechat.SendKeys('{Enter}')
        print("已发送")
    else:
        print("已输入文本框（未发送）")

def send_files(wechat, file_paths):
    """发送多个文件（一次性复制到剪贴板，批量粘贴）"""
    # 用 PowerShell Set-Clipboard 一次性复制多个文件
    paths_json = ','.join(f'"{p}"' for p in file_paths)
    ps_cmd = f'Set-Clipboard -Path @({paths_json})'
    print(f"正在复制 {len(file_paths)} 个文件到剪贴板...")
    subprocess.run(['powershell', '-Command', ps_cmd], shell=True)
    time.sleep(1)
    wechat.SendKeys('{Ctrl}v')
    time.sleep(3)  # 多文件粘贴需要更长时间
    wechat.SendKeys('{Enter}')
    time.sleep(1)
    print(f"{len(file_paths)} 个文件已发送")


def main():
    # 参数解析
    recipient = None
    file_paths = []
    text_content = None
    mode = 'text'
    no_send = False
    
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == '--mode':
            i += 1
            mode = args[i] if i < len(args) else 'text'
        elif args[i] == '--no-send':
            no_send = True
        elif recipient is None:
            recipient = args[i]
        elif mode == 'file':
            # file 模式下，所有剩余参数都是文件路径
            file_paths.append(args[i])
        elif text_content is None:
            text_content = args[i]
        i += 1
    
    if not recipient:
        print("用法: python send_wechat.py \"收件人\" \"内容\" [--mode file] [--no-send]")
        return
    
    print(f"收件人: {recipient}")
    print(f"模式: {mode}")
    if mode == 'file':
        print(f"文件数: {len(file_paths)}
    
    # 查找/启动微信
    wechat = None
    for retry in range(3):
        wechat = find_wechat()
        if wechat:
            break
        time.sleep(2)
    
    if not wechat:
        print("未找到微信窗口，启动中...")
        subprocess.Popen(WECHAT_PATH)
        for retry in range(8):
            time.sleep(2)
            wechat = find_wechat()
            if wechat:
                break
    
    if not wechat:
        print("错误：无法找到微信窗口")
        return
    
    print(f"找到微信窗口 | PID={wechat.ProcessId}")
    
    # 激活
    activate_window(wechat)
    active = auto.GetForegroundControl()
    print(f"当前活动窗口: {active.ClassName}")
    
    # 搜索联系人
    search_and_open(wechat, recipient)
    
    # 发送
    if mode == 'file' and file_paths:
        send_files(wechat, file_paths)
    elif mode == 'text' and text_content:
        send_text(wechat, text_content, no_send)
    else:
        # 没有指定内容，粘贴剪贴板
        print("粘贴剪贴板内容...")
        wechat.SendKeys('{Ctrl}v')
        time.sleep(1.5)
        wechat.SendKeys('{Enter}')
        print("已发送")

if __name__ == '__main__':
    main()
