#!/bin/bash

###############################################################################
# ClamAV GUI Pro - MX Linux Installer
# Created by: Arlindo Pereira
# Email: Ajcppt@aol.com
# Version: 3.0
# 
# Specifically for MX Linux and other SysVinit-based systems
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
    echo -e "${BLUE}   ClamAV GUI Pro - MX Linux Installer v3.0${NC}"
    echo -e "${BLUE}================================================${NC}"
    echo ""
}

print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    print_error "Do not run as root. Script will ask for sudo when needed."
    exit 1
fi

print_header

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
print_info "Installation files location: $SCRIPT_DIR"

# Check if clamav_gui_pro.py exists
if [ ! -f "$SCRIPT_DIR/clamav_gui_pro.py" ]; then
    print_error "clamav_gui_pro.py not found in $SCRIPT_DIR"
    print_info "Please run this script from the directory containing the installation files"
    exit 1
fi

# Check Python
print_info "Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python $PYTHON_VERSION found"
else
    print_error "Python 3 not found"
    print_info "Please install Python 3 first: sudo apt install python3 python3-pip"
    exit 1
fi

# Check ClamAV
print_info "Checking ClamAV..."
if command -v clamscan &> /dev/null; then
    CLAMAV_VERSION=$(clamscan --version | cut -d' ' -f2)
    print_success "ClamAV $CLAMAV_VERSION found"
else
    print_warning "ClamAV not found. Installing..."
    sudo apt update
    sudo apt install -y clamav clamav-daemon
    print_success "ClamAV installed"
fi

# Check and start ClamAV daemon (MX Linux uses SysVinit)
print_info "Checking ClamAV daemon..."
if [ -f /etc/init.d/clamav-daemon ]; then
    sudo /etc/init.d/clamav-daemon start 2>/dev/null || print_warning "ClamAV daemon may already be running"
    print_success "ClamAV daemon configured"
elif command -v systemctl &> /dev/null; then
    # Fallback for systems with systemd
    sudo systemctl enable clamav-daemon 2>/dev/null || true
    sudo systemctl start clamav-daemon 2>/dev/null || true
    print_success "ClamAV daemon configured (systemd)"
else
    print_warning "Could not start ClamAV daemon automatically"
    print_info "You may need to start it manually for real-time protection"
fi

# Update virus databases
print_info "Updating virus databases (this may take a few minutes)..."
sudo freshclam 2>/dev/null || print_warning "Database update will be done on first run"

# Install PyQt6
print_info "Installing PyQt6..."
pip3 install --user PyQt6 2>/dev/null || {
    print_warning "pip install failed, trying with apt..."
    sudo apt install -y python3-pyqt6 2>/dev/null || print_warning "PyQt6 installation may have failed"
}
print_success "PyQt6 installation attempted"

# Create installation directory
INSTALL_DIR="$HOME/clamav-gui-pro"
print_info "Installing to $INSTALL_DIR..."
mkdir -p "$INSTALL_DIR"

# Copy files
print_info "Copying files..."
cp "$SCRIPT_DIR/clamav_gui_pro.py" "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/clamav_gui_pro.py"

if [ -f "$SCRIPT_DIR/uninstall.sh" ]; then
    cp "$SCRIPT_DIR/uninstall.sh" "$INSTALL_DIR/"
    chmod +x "$INSTALL_DIR/uninstall.sh"
fi

if [ -f "$SCRIPT_DIR/uninstall-mx-linux.sh" ]; then
    cp "$SCRIPT_DIR/uninstall-mx-linux.sh" "$INSTALL_DIR/"
    chmod +x "$INSTALL_DIR/uninstall-mx-linux.sh"
fi

print_success "Files copied"

# Create configuration directories
CONFIG_DIR="$HOME/.clamav-gui"
mkdir -p "$CONFIG_DIR"
mkdir -p "$CONFIG_DIR/quarantine"
print_success "Configuration directory created at $CONFIG_DIR"

# Create launcher
print_info "Creating launcher..."
LAUNCHER="$HOME/.local/bin/clamav-gui-pro"
mkdir -p "$HOME/.local/bin"

cat > "$LAUNCHER" << 'LAUNCHER_EOF'
#!/bin/bash
cd "$HOME/clamav-gui-pro"
python3 clamav_gui_pro.py "$@"
LAUNCHER_EOF

chmod +x "$LAUNCHER"
print_success "Launcher created"

# Create desktop entry
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

# Update desktop database if available
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true
fi

# Add to PATH if not already there
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    print_info "Adding $HOME/.local/bin to PATH..."
    
    # Detect shell
    if [ -n "$BASH_VERSION" ]; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
        print_warning "Please run: source ~/.bashrc"
    elif [ -n "$ZSH_VERSION" ]; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc"
        print_warning "Please run: source ~/.zshrc"
    else
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.profile"
        print_warning "Please restart your terminal or run: source ~/.profile"
    fi
fi

# Remove old installation from /opt if exists
if [ -f /opt/clamav_gui_pro.py ]; then
    print_warning "Old installation found in /opt"
    read -p "Remove old version from /opt? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo rm /opt/clamav_gui_pro.py
        print_success "Old version removed"
    fi
fi

# Installation complete
echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}   Installation Complete! 🎉${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
print_success "ClamAV GUI Pro has been installed successfully!"
echo ""
print_info "You can now run it by:"
echo "  1. Searching for 'ClamAV GUI Pro' in your application menu"
echo "  2. Running: clamav-gui-pro"
echo "  3. Running: python3 $INSTALL_DIR/clamav_gui_pro.py"
echo ""
print_info "MX Linux specific notes:"
echo "  • ClamAV daemon uses SysVinit (not systemd)"
echo "  • To check daemon status: sudo /etc/init.d/clamav-daemon status"
echo "  • To restart daemon: sudo /etc/init.d/clamav-daemon restart"
echo ""
print_info "First-time setup:"
echo "  • Update virus databases from the Update tab"
echo "  • Configure real-time protection in Settings"
echo ""
print_info "To uninstall later:"
if [ -f "$INSTALL_DIR/uninstall-mx-linux.sh" ]; then
    echo "  Run: $INSTALL_DIR/uninstall-mx-linux.sh"
else
    echo "  Run: $INSTALL_DIR/uninstall.sh"
fi
echo ""
print_warning "Some features require administrator privileges and will prompt for your password"
echo ""

# Ask if user wants to launch now
read -p "Launch ClamAV GUI Pro now? (Y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    python3 "$INSTALL_DIR/clamav_gui_pro.py" &
    print_success "Application launched!"
fi

echo ""
print_info "Thank you for installing ClamAV GUI Pro!"
print_info "Created by: Arlindo Pereira (Ajcppt@aol.com)"
echo ""
