#!/bin/bash

###############################################################################
# ClamAV GUI Pro - Uninstaller
# Created by: Arlindo Pereira
# Email: Ajcppt@aol.com
# Version: 3.0
###############################################################################

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE}   ClamAV GUI Pro - Uninstaller${NC}"
    echo -e "${BLUE}================================================${NC}"
    echo ""
}

print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }

print_header

INSTALL_DIR="$HOME/clamav-gui-pro"
CONFIG_DIR="$HOME/.clamav-gui"

if [ ! -d "$INSTALL_DIR" ] && [ ! -d "$CONFIG_DIR" ]; then
    print_warning "ClamAV GUI Pro not installed"
    exit 0
fi

echo -e "${YELLOW}This will remove ClamAV GUI Pro${NC}"
echo ""
read -p "Continue? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_info "Cancelled"
    exit 0
fi

echo ""
print_info "Uninstalling..."

pkill -f "clamav_gui_pro.py" 2>/dev/null || true
print_success "Stopped running instances"

if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    print_success "Removed application files"
fi

DESKTOP_FILE="$HOME/.local/share/applications/clamav-gui-pro.desktop"
if [ -f "$DESKTOP_FILE" ]; then
    rm -f "$DESKTOP_FILE"
    print_success "Removed desktop entry"
fi

LAUNCHER="$HOME/.local/bin/clamav-gui-pro"
if [ -f "$LAUNCHER" ]; then
    rm -f "$LAUNCHER"
    print_success "Removed launcher"
fi

echo ""
if [ -d "$CONFIG_DIR" ]; then
    echo "Configuration location: $CONFIG_DIR"
    if [ -d "$CONFIG_DIR/quarantine" ]; then
        QUARANTINE_COUNT=$(find "$CONFIG_DIR/quarantine" -type f ! -name "*.json" 2>/dev/null | wc -l)
        if [ "$QUARANTINE_COUNT" -gt 0 ]; then
            echo "  • $QUARANTINE_COUNT quarantined file(s)"
        fi
    fi
    echo ""
    read -p "Remove configuration and quarantine? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$CONFIG_DIR"
        print_success "Configuration removed"
    else
        print_info "Configuration preserved at: $CONFIG_DIR"
    fi
fi

echo ""
read -p "Remove ClamAV engine? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    sudo apt remove --purge -y clamav clamav-daemon 2>/dev/null || true
    print_success "ClamAV removed"
else
    print_info "ClamAV preserved"
fi

echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}   Uninstallation Complete${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
print_success "ClamAV GUI Pro uninstalled"
echo ""
print_info "Thank you for using ClamAV GUI Pro!"
print_info "Created by: Arlindo Pereira (Ajcppt@aol.com)"
echo ""
