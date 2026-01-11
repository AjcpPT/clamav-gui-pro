# 🛡️ ClamAV GUI Pro

[![GitHub release](https://img.shields.io/github/v/release/AjcpPT/clamav-gui-pro)](https://github.com/AjcpPT/clamav-gui-pro/releases)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![GitHub issues](https://img.shields.io/github/issues/AjcpPT/clamav-gui-pro)](https://github.com/AjcpPT/clamav-gui-pro/issues)
[![GitHub stars](https://img.shields.io/github/stars/AjcpPT/clamav-gui-pro)](https://github.com/AjcpPT/clamav-gui-pro/stargazers)

**Professional Graphical Interface for ClamAV Antivirus**

---

## 🌟 Features

### Core Features
- ✅ **Real-time Protection** - Monitor files as they're created/modified
- ✅ **Automatic Quarantine** - Isolate infected files automatically
- ✅ **Scheduled Scans** - Set daily, weekly, or monthly scans
- ✅ **Multiple Database Sources** - Official ClamAV + free community databases
- ✅ **Custom Databases** - Add paid or proprietary signature databases
- ✅ **Statistics & Reports** - Track scans and threats over time
- ✅ **Context Menu Integration** - Right-click to scan files
- ✅ **Auto-Update System** - Keep both virus databases and program updated
- ✅ **Multi-language Support** - English and Portuguese (more coming soon)

### Advanced Features
- 🔒 **Quarantine Manager** - Restore or permanently delete quarantined files
- 🚫 **Exclusions List** - Skip trusted files and folders
- 📊 **Detailed Statistics** - Visual graphs of scan history
- 📤 **Export Logs** - Generate HTML reports
- 🔕 **Silent Mode** - Run scans in background
- 🔔 **Desktop Notifications** - Get alerts about threats
- ⚙️ **Flexible Settings** - Customize every aspect

---

## ## 📋 Requirements

- **OS**: Linux (Ubuntu/Debian-based, MX Linux, AntiX, Devuan)
- **Python**: 3.8 or higher
- **ClamAV**: Automatically installed if missing
- **PyQt6**: Automatically installed if missing

---

## 🚀 Quick Install

### For Most Linux Distributions (Ubuntu, Debian, Fedora, Pop!_OS, etc.)

```bash
# Download the installer
wget https://raw.githubusercontent.com/AjcpPT/clamav-gui-pro/main/install.sh

# Make it executable
chmod +x install.sh

# Run installer
./install.sh
```

### For MX Linux / AntiX / Devuan (SysVinit-based systems)

```bash
# Download the MX Linux installer
wget https://raw.githubusercontent.com/AjcpPT/clamav-gui-pro/main/install-mx-linux.sh

# Make it executable
chmod +x install-mx-linux.sh

# Run installer
./install-mx-linux.sh
```

### Manual Installation

```bash
# Clone repository
git clone https://github.com/AjcpPT/clamav-gui-pro.git
cd clamav-gui-pro

# Install dependencies
sudo apt update
sudo apt install -y clamav clamav-daemon python3 python3-pip

# Install Python dependencies
pip3 install --user PyQt6

# Run the application
python3 clamav_gui_pro.py
```

---

## 💻 Usage

### Launch Application

```bash
# From installation directory
python3 clamav_gui_pro.py

# Or if installed system-wide
clamav-gui-pro

# Or from application menu
# Search for "ClamAV GUI Pro"
```

### First Run

On first launch, you'll see a warning about administrator permissions. Some operations require `sudo`:
- Updating virus databases
- Real-time protection
- System-wide scans

You'll be prompted for your password when needed.

### Quick Scan

1. Click **⚡ Quick Scan** to scan common locations (Downloads, Desktop, Documents)
2. Or use **Ctrl+Shift+Q**

### Custom Scan

1. Click **📁 Scan Folder** to choose a specific directory
2. Enable **recursive scan** to include subfolders
3. Enable **quarantine** to automatically isolate threats

### Update Databases

**Important:** There are TWO types of updates:

#### 🦠 Update Virus Databases
- Updates ClamAV signature databases
- Click **Update → Update Virus Databases**
- Or press **Ctrl+U**

#### 🔄 Update ClamAV GUI Pro Program
- Updates the application itself
- Click **Update → Update Program**
- Downloads latest version from GitHub

### Real-time Protection

1. Go to **🛡️ Real-time** tab
2. Enable **Real-time Protection**
3. Choose folders to monitor (Downloads, Documents, etc.)
4. Threats will be detected and quarantined automatically

### Quarantine Management

1. Go to **🔒 Quarantine** tab
2. View all quarantined files
3. **Restore** files if they're false positives
4. **Delete Permanently** to remove threats

### Schedule Scans

1. Go to **⚙️ Settings** tab
2. Add scheduled scans (daily, weekly, monthly)
3. Choose time and path to scan
4. Scans run automatically in background

---

## 🌐 Language Support

Switch between languages in **Options → Language**:
- 🇬🇧 English (default)
- 🇵🇹 Português

More languages coming soon!

---

## 📊 Database Sources

### Official ClamAV Databases (Always Enabled)
- `main.cvd` - Main virus database
- `daily.cvd` - Daily updates
- `bytecode.cvd` - Bytecode signatures

### Free Community Databases (Optional)
- **Sanesecurity** - Spam, phishing, malware
- **URLhaus** - Malicious URLs
- **MalwarePatrol** - Recent threats (free tier)

### Custom Databases
Add paid or proprietary databases:
1. Go to **🔄 Update** tab
2. Click **➕ Add Custom Database**
3. Enter database URL or path
4. Database will be downloaded and integrated

---

## 🔧 Configuration

Configuration files are stored in: `~/.clamav-gui/`

- `language.json` - Language preference
- `last_update.json` - Last database update timestamp
- `scan_history.json` - Scan history and statistics
- `quarantine/` - Quarantined files directory
- `first_run.json` - First-run warning flag

---

## 🐛 Troubleshooting

### ClamAV not detected
```bash
sudo apt install clamav clamav-daemon
sudo systemctl start clamav-daemon
sudo systemctl enable clamav-daemon
```

### Database update fails
```bash
sudo freshclam
```

### Permission errors
Make sure to run with proper permissions:
```bash
# For system-wide scans
sudo python3 clamav_gui_pro.py
```

### Real-time protection not working
Enable ClamAV daemon:
```bash
sudo systemctl enable clamav-daemon
sudo systemctl start clamav-daemon
```

---

## 🔄 Updating

The application checks for updates automatically. You can also:

1. **Manual check**: Click **Update → Update Program**
2. **Command line**:
```bash
cd clamav-gui-pro
git pull origin main
python3 clamav_gui_pro.py
```

---

## 🗑️ Uninstall

```bash
# Run uninstaller
./uninstall.sh

# Or manually
rm -rf ~/.clamav-gui
rm ~/.local/share/applications/clamav-gui-pro.desktop
rm ~/clamav-gui-pro  # or your installation directory
```

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the **GPL-3.0 License** - see the [LICENSE](LICENSE) file for details.

ClamAV itself is also GPL-licensed by Cisco Systems.

---

## 👨‍💻 Author

**Arlindo Pereira**
- Email: Ajcppt@aol.com
- GitHub: [@YourUsername](https://github.com/YourUsername)

---

## 🙏 Acknowledgments

- **ClamAV Team** - For the excellent open-source antivirus engine
- **Sanesecurity** - For free additional databases
- **URLhaus** - For malicious URL database
- **PyQt6** - For the GUI framework

---

## 📸 Screenshots

### Main Scan Interface
![Scan Tab](screenshots/scan_tab.png)

### Real-time Protection
![Real-time](screenshots/realtime.png)

### Quarantine Manager
![Quarantine](screenshots/quarantine.png)

### Statistics
![Statistics](screenshots/statistics.png)

---

## ⚠️ Disclaimer

This software is provided "as is" without warranty of any kind. While ClamAV is a robust antivirus solution, no antivirus can guarantee 100% detection. Always practice safe computing habits.

---

## 🔗 Links

- [ClamAV Official Site](https://www.clamav.net/)
- [ClamAV Documentation](https://docs.clamav.net/)
- [Report Issues](https://github.com/YourUsername/clamav-gui-pro/issues)
- [Request Features](https://github.com/YourUsername/clamav-gui-pro/issues/new)

---

**Made with ❤️ for the Linux community**
