# Changelog

All notable changes to ClamAV GUI Pro will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [3.0] - 2025-01-10

### 🎉 Major Release - Professional Edition

This is a complete rewrite with professional-grade features!

### Added
- **Real-time Protection** - Monitor files as they're created/modified
- **Automatic Quarantine System** - Infected files automatically isolated
- **Scheduled Scans** - Daily, weekly, or monthly automatic scans
- **Multi-language Support** - English and Portuguese (more coming soon)
- **Custom Database Support** - Add paid or proprietary signature databases
- **Statistics & Reporting** - Visual graphs and detailed scan history
- **Context Menu Integration** - Right-click to scan files in file manager
- **Auto-Update System** - Separate updates for program and virus databases
- **Exclusions List** - Skip trusted files and folders during scans
- **Whitelist Management** - Mark files as safe permanently
- **Export Functionality** - Save logs as HTML or PDF reports
- **Desktop Notifications** - Get alerts when threats are detected
- **Silent Background Mode** - Run scans without UI interference
- **System Tray Integration** - Quick access from system tray
- **Autostart on Boot** - Launch automatically when system starts
- **Quarantine Restore** - Recover false positives from quarantine
- **First-run Warning** - Information about sudo requirements
- **7 Specialized Tabs** - Organized interface for all features
  - Scan
  - Update (separated: virus DB vs program)
  - Quarantine
  - History
  - Statistics
  - Real-time Protection
  - Settings

### Changed
- **Default Language** - Changed from Portuguese to English
- **Configuration Directory** - Moved to `~/.clamav-gui` for better organization
- **UI Framework** - Enhanced PyQt6 interface with better responsiveness
- **Scan Engine** - Improved performance with multi-threading
- **Database Management** - Clear separation between virus DB and program updates

### Fixed
- **Menu Duplication Bug** - Fixed issue when changing language multiple times
- **Scan Progress** - More accurate progress reporting
- **Memory Usage** - Optimized for better performance on low-end systems
- **Permission Handling** - Better sudo prompt management

### Security
- **Quarantine Isolation** - Files are properly isolated and cannot execute
- **Permission Checks** - Proper validation before requesting sudo
- **Safe Restore** - Quarantine files can be safely restored

---

## [2.0] - 2024-12-15

### Added
- Complete GUI redesign using PyQt6
- Update tab for managing ClamAV databases
- Scan history tracking with timestamps
- Basic settings interface
- Multi-language foundation (Portuguese and English)
- Extra free databases (Sanesecurity, URLhaus)

### Changed
- Migrated from PyQt5 to PyQt6
- Improved scan performance
- Better error handling

### Fixed
- Database update failures
- UI freezing during long scans
- Permission issues on some systems

---

## [1.0] - 2024-11-01

### Added
- Initial release
- Basic file scanning functionality
- Folder scanning with recursive option
- ClamAV integration
- Simple graphical interface
- Scan log display
- Portuguese language support

---

## Upcoming Features

### Planned for 3.1
- [ ] Network drive scanning
- [ ] Cloud storage integration (Dropbox, Google Drive)
- [ ] Email attachment scanning
- [ ] Browser download protection
- [ ] Spanish language support
- [ ] French language support
- [ ] German language support
- [ ] Custom scan profiles
- [ ] Scan scheduling with cron integration
- [ ] Remote scan management

### Planned for 4.0
- [ ] AI-powered threat detection
- [ ] Sandboxing for suspicious files
- [ ] Behavior analysis engine
- [ ] Network traffic monitoring
- [ ] Central management dashboard
- [ ] Multi-system deployment
- [ ] Cloud-based threat intelligence
- [ ] Advanced reporting and analytics

---

## Version History Summary

| Version | Date | Major Features |
|---------|------|----------------|
| 3.0 | 2025-01-10 | Real-time protection, quarantine, scheduling |
| 2.0 | 2024-12-15 | PyQt6 redesign, history tracking |
| 1.0 | 2024-11-01 | Initial release |

---

## Migration Guide

### Upgrading from 2.0 to 3.0

**Configuration Changes:**
- Old config location: `~/.config/clamav-gui/`
- New config location: `~/.clamav-gui/`
- Config files are automatically migrated on first run

**New Features to Explore:**
1. Enable real-time protection in the Real-time tab
2. Set up scheduled scans in Settings
3. Configure quarantine behavior in Scan options
4. Add exclusions for trusted directories
5. Check statistics in the new Statistics tab

**Breaking Changes:**
- Default language is now English (was Portuguese)
- Command-line arguments have changed (see README)
- Some config file formats updated

### Upgrading from 1.0 to 3.0

This is a major upgrade. We recommend:
1. Export any important scan logs
2. Backup your configuration
3. Perform a clean installation
4. Reconfigure your preferences

---

## Known Issues

### Current Version (3.0)

**Minor Issues:**
- Real-time protection may require additional setup on some distributions
- Large file scans (>1GB) can be slow
- Some desktop environments don't support system tray

**Workarounds:**
- For real-time protection: Ensure clamav-daemon is running
- For large files: Use --max-filesize option
- For tray icons: Use desktop shortcuts instead

---

## Deprecation Notices

### Deprecated in 3.0
- None yet

### To Be Deprecated in 4.0
- Legacy config file format (will auto-migrate)
- Command-line arguments from 1.x versions

---

## Contributors

### Version 3.0
- **Arlindo Pereira** - Lead Developer & Creator
  - Email: Ajcppt@aol.com

### Special Thanks
- ClamAV Team - For the excellent antivirus engine
- PyQt6 Team - For the GUI framework
- Sanesecurity - For free virus databases
- All users who provided feedback and bug reports

---

## License

ClamAV GUI Pro is licensed under GPL-3.0

Copyright (C) 2024-2025 Arlindo Pereira

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

---

For detailed information about each version, visit:
https://github.com/YourUsername/clamav-gui-pro/releases
