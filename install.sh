#!/bin/bash

###############################################################################
# ClamAV GUI Pro - Installation Script
# Created by: Arlindo Pereira
# Email: Ajcppt@aol.com
# Version: 3.0
###############################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE}   ClamAV GUI Pro - Installer v3.0${NC}"
    echo -e "${BLUE}================================================${NC}"
    echo ""
}

print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }

if [ "$EUID" -eq 0 ]; then 
    print_error "Do not run as root. Script will ask for sudo when needed."
    exit 1
fi

print_header

print_info "Checking system..."
if ! command -v apt &> /dev/null; then
    print_error "This installer requires apt (Debian/Ubuntu based)"
    exit 1
fi

print_info "Checking Python..."
if command -v python3 &> /dev/null; then
    print_success "Python $(python3 --version | cut -d' ' -f2) found"
else
    print_info "Installing Python 3..."
    sudo apt update
    sudo apt install -y python3 python3-pip
fi

print_info "Checking ClamAV..."
if command -v clamscan &> /dev/null; then
    print_success "ClamAV $(clamscan --version | cut -d' ' -f2) already installed"
else
    print_warning "Installing ClamAV..."
    sudo apt update
    sudo apt install -y clamav clamav-daemon
    print_success "ClamAV installed"
fi

print_info "Configuring ClamAV daemon..."
sudo systemctl stop clamav-freshclam 2>/dev/null || true
sudo systemctl enable clamav-daemon
sudo systemctl start clamav-daemon
print_success "ClamAV daemon configured"

print_info "Updating virus databases..."
sudo freshclam || print_warning "Update on first run"

print_info "Installing PyQt6..."
pip3 install --user PyQt6 || sudo apt install -y python3-pyqt6
print_success "PyQt6 installed"

INSTALL_DIR="$HOME/clamav-gui-pro"
print_info "Installing to $INSTALL_DIR..."
mkdir -p "$INSTALL_DIR"

if [ -f "clamav_gui_pro.py" ]; then
    cp clamav_gui_pro.py "$INSTALL_DIR/"
    chmod +x "$INSTALL_DIR/clamav_gui_pro.py"
else
    print_error "clamav_gui_pro.py not found in current directory"
    exit 1
fi

CONFIG_DIR="$HOME/.clamav-gui"
mkdir -p "$CONFIG_DIR"
mkdir -p "$CONFIG_DIR/quarantine"
print_success "Configuration directory created"

print_info "Creating desktop entry..."
DESKTOP_FILE="$HOME/.local/share/applications/clamav-gui-pro.desktop"
mkdir -p "$HOME/.local/share/applications"

cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=3.0
Type=Application
Name=ClamAV GUI Pro
GenericName=Antivirus
Comment=Professional antivirus with real-time protection
Exec=python3 $INSTALL_DIR/clamav_gui_pro.py
Icon=security-medium
Terminal=false
Categories=System;Security;
Keywords=antivirus;security;scan;malware;
StartupNotify=true
EOF

chmod +x "$DESKTOP_FILE"
print_success "Desktop entry created"

print_info "Creating launcher..."
LAUNCHER="$HOME/.local/bin/clamav-gui-pro"
mkdir -p "$HOME/.local/bin"

cat > "$LAUNCHER" << EOF
#!/bin/bash
cd "$INSTALL_DIR"
python3 clamav_gui_pro.py "\$@"
EOF

chmod +x "$LAUNCHER"
print_success "Launcher created"

if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
    print_warning "Run: source ~/.bashrc"
fi

echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}   Installation Complete! 🎉${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
print_success "ClamAV GUI Pro installed successfully!"
echo ""
print_info "Run with: clamav-gui-pro"
print_info "Or search 'ClamAV GUI Pro' in applications"
echo ""

read -p "Launch now? (Y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    python3 "$INSTALL_DIR/clamav_gui_pro.py" &
    print_success "Launched!"
fi

echo ""
print_info "Created by: Arlindo Pereira (Ajcppt@aol.com)"
echo ""
