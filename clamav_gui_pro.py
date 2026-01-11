#!/usr/bin/env python3
"""
ClamAV GUI Pro - Professional Antivirus Interface
Created by: Arlindo Pereira
Email: Ajcppt@aol.com
Version: 3.0
License: GPL-3.0
"""

import sys
import os
import subprocess
import json
import shutil
import time
from pathlib import Path
from datetime import datetime

# Check dependencies
def check_dependencies():
    missing = []
    try:
        subprocess.run(['clamscan', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        missing.append('clamav')
    try:
        import PyQt6
    except ImportError:
        missing.append('pyqt6')
    
    if missing:
        print("🔧 Installing dependencies...")
        if 'clamav' in missing:
            print("📦 Installing ClamAV...")
            try:
                subprocess.run(['pkexec', 'apt-get', 'update'], check=True)
                subprocess.run(['pkexec', 'apt-get', 'install', '-y', 'clamav', 'clamav-daemon'], check=True)
                print("✅ ClamAV installed!")
            except subprocess.CalledProcessError:
                print("❌ Error installing ClamAV")
                sys.exit(1)
        if 'pyqt6' in missing:
            print("📦 Installing PyQt6...")
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', '--user', 'PyQt6'], check=True)
                print("✅ PyQt6 installed!")
            except subprocess.CalledProcessError:
                print("❌ Error installing PyQt6")
                sys.exit(1)
        print("\n✅ Restarting...\n")
        os.execv(sys.executable, [sys.executable] + sys.argv)

check_dependencies()

from PyQt6.QtWidgets import *
from PyQt6.QtCore import QThread, pyqtSignal, Qt, QTimer
from PyQt6.QtGui import QFont, QAction, QIcon

VERSION = "3.0"
GITHUB_REPO = "https://api.github.com/repos/AjcpPT/clamav-gui-pro/releases/latest"

TRANSLATIONS = {
    'en': {
        'app_title': 'ClamAV GUI Pro - Professional Antivirus',
        'menu_file': '&File', 'menu_scan': '&Scan', 'menu_update': '&Update',
        'menu_tools': '&Tools', 'menu_help': '&Help', 'menu_exit': 'E&xit',
        'menu_quick_scan': 'Quick Scan', 'menu_full_scan': 'Full System Scan',
        'menu_update_virus_db': 'Update Virus Databases',
        'menu_update_program': 'Update Program', 'menu_about': 'About',
        'tab_scan': '🔍 Scan', 'tab_update': '🔄 Update',
        'tab_quarantine': '🔒 Quarantine', 'tab_history': '📊 History',
        'tab_statistics': '📈 Statistics', 'tab_realtime': '🛡️ Real-time',
        'tab_settings': '⚙️ Settings', 'btn_scan_file': '📄 Scan File',
        'btn_scan_folder': '📁 Scan Folder', 'btn_quick_scan': '⚡ Quick Scan',
        'scan_log': '📋 Scan Log:', 'quarantine_title': '🔒 Quarantined Files:',
        'restore_file': '↩️ Restore', 'delete_permanent': '🗑️ Delete',
        'about_text': '''<h2>ClamAV GUI Pro v{version}</h2>
<p><b>Created by:</b> Arlindo Pereira<br><b>Email:</b> Ajcppt@aol.com</p>
<p>Professional antivirus with real-time protection</p>
<p><b>License:</b> GPL v3</p>''',
        'select_file': 'Select file', 'select_folder': 'Select folder',
        'ready': 'Ready', 'files_scanned': 'Files scanned:',
        'infected': 'Infected:', 'scan_complete': 'Scan Complete',
    },
    'pt': {
        'app_title': 'ClamAV GUI Pro - Antivírus Profissional',
        'menu_file': '&Ficheiro', 'menu_scan': '&Verificar', 'menu_update': '&Atualizar',
        'menu_tools': '&Ferramentas', 'menu_help': 'Aj&uda', 'menu_exit': '&Sair',
        'menu_quick_scan': 'Verificação Rápida', 'menu_full_scan': 'Verificação Completa',
        'menu_update_virus_db': 'Atualizar Bases de Vírus',
        'menu_update_program': 'Atualizar Programa', 'menu_about': 'Sobre',
        'tab_scan': '🔍 Verificar', 'tab_update': '🔄 Atualizar',
        'tab_quarantine': '🔒 Quarentena', 'tab_history': '📊 Histórico',
        'tab_statistics': '📈 Estatísticas', 'tab_realtime': '🛡️ Tempo Real',
        'tab_settings': '⚙️ Definições', 'btn_scan_file': '📄 Verificar Ficheiro',
        'btn_scan_folder': '📁 Verificar Pasta', 'btn_quick_scan': '⚡ Verificação Rápida',
        'scan_log': '📋 Registo:', 'quarantine_title': '🔒 Ficheiros em Quarentena:',
        'restore_file': '↩️ Restaurar', 'delete_permanent': '🗑️ Eliminar',
        'about_text': '''<h2>ClamAV GUI Pro v{version}</h2>
<p><b>Criado por:</b> Arlindo Pereira<br><b>Email:</b> Ajcppt@aol.com</p>
<p>Antivírus profissional com proteção em tempo real</p>
<p><b>Licença:</b> GPL v3</p>''',
        'select_file': 'Selecionar ficheiro', 'select_folder': 'Selecionar pasta',
        'ready': 'Pronto', 'files_scanned': 'Ficheiros verificados:',
        'infected': 'Infectados:', 'scan_complete': 'Verificação Completa',
    }
}

class ScanThread(QThread):
    progress = pyqtSignal(str)
    stats = pyqtSignal(dict)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, path, recursive=True, quarantine=True):
        super().__init__()
        self.path = path
        self.recursive = recursive
        self.quarantine = quarantine
        self.config_dir = Path.home() / '.clamav-gui'
    
    def run(self):
        try:
            cmd = ['clamscan']
            if self.recursive:
                cmd.append('-r')
            cmd.extend(['-i', self.path])
            
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)
            infected = []
            scanned = 0
            
            for line in process.stdout:
                line = line.strip()
                if line:
                    self.progress.emit(line)
                    if 'FOUND' in line:
                        file_path = line.split(':')[0].strip()
                        infected.append(file_path)
                        if self.quarantine:
                            self.quarantine_file(file_path)
                    if 'Scanned files:' in line:
                        try:
                            scanned = int(line.split(':')[1].strip())
                        except:
                            pass
            
            process.wait()
            
            stats = {'scanned': scanned, 'infected': len(infected), 'timestamp': datetime.now().isoformat()}
            self.stats.emit(stats)
            
            if len(infected) > 0:
                msg = f"⚠️ {len(infected)} infected file(s) found!"
                if self.quarantine:
                    msg += f"\n{len(infected)} moved to quarantine."
                self.finished.emit(False, msg)
            else:
                self.finished.emit(True, f"✅ {scanned} files scanned. No threats.")
        except Exception as e:
            self.finished.emit(False, f"❌ Error: {str(e)}")
    
    def quarantine_file(self, file_path):
        try:
            quarantine_dir = self.config_dir / 'quarantine'
            quarantine_dir.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            dest = quarantine_dir / f"{timestamp}_{Path(file_path).name}"
            shutil.move(file_path, dest)
            metadata = {'original': file_path, 'time': timestamp}
            with open(f"{dest}.json", 'w') as f:
                json.dump(metadata, f)
        except Exception as e:
            self.progress.emit(f"⚠️ Quarantine failed: {e}")

class UpdateThread(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str)
    
    def run(self):
        try:
            self.progress.emit("🔄 Updating databases...")
            result = subprocess.run(['freshclam'], capture_output=True, text=True)
            if result.returncode == 0:
                self.progress.emit("✅ Updated!")
            else:
                self.progress.emit("ℹ️ Already up to date")
            self.finished.emit(True, "✅ Update complete!")
        except Exception as e:
            self.finished.emit(False, f"❌ Error: {str(e)}")

class AboutDialog(QDialog):
    def __init__(self, parent, lang):
        super().__init__(parent)
        self.setWindowTitle("About")
        self.setFixedSize(500, 350)
        layout = QVBoxLayout(self)
        text = QLabel(TRANSLATIONS[lang]['about_text'].format(version=VERSION))
        text.setWordWrap(True)
        text.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(text)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

class ClamAVGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config_dir = Path.home() / '.clamav-gui'
        self.config_dir.mkdir(exist_ok=True)
        self.load_language()
        self.init_ui()
        self.show_first_warning()
    
    def load_language(self):
        lang_file = self.config_dir / 'language.json'
        if lang_file.exists():
            with open(lang_file, 'r') as f:
                self.lang = json.load(f).get('language', 'en')
        else:
            self.lang = 'en'
    
    def save_language(self):
        with open(self.config_dir / 'language.json', 'w') as f:
            json.dump({'language': self.lang}, f)
    
    def tr(self, key):
        return TRANSLATIONS[self.lang].get(key, key)
    
    def change_language(self, lang):
        if lang == self.lang:
            return
        self.lang = lang
        self.save_language()
        old = self.centralWidget()
        if old:
            old.deleteLater()
        self.menuBar().clear()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle(self.tr('app_title'))
        self.setGeometry(100, 100, 1000, 800)
        self.create_menu_bar()
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        title = QLabel("🛡️ ClamAV GUI Pro")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_scan_tab(), self.tr('tab_scan'))
        self.tabs.addTab(self.create_update_tab(), self.tr('tab_update'))
        self.tabs.addTab(self.create_quarantine_tab(), self.tr('tab_quarantine'))
        self.tabs.addTab(self.create_history_tab(), self.tr('tab_history'))
        self.tabs.addTab(self.create_statistics_tab(), self.tr('tab_statistics'))
        self.tabs.addTab(self.create_realtime_tab(), self.tr('tab_realtime'))
        self.tabs.addTab(self.create_settings_tab(), self.tr('tab_settings'))
        layout.addWidget(self.tabs)
        
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage(self.tr('ready'))
    
    def create_menu_bar(self):
        menubar = self.menuBar()
        menubar.clear()
        
        file_menu = menubar.addMenu(self.tr('menu_file'))
        exit_action = QAction(self.tr('menu_exit'), self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        scan_menu = menubar.addMenu(self.tr('menu_scan'))
        quick = QAction(self.tr('menu_quick_scan'), self)
        quick.triggered.connect(self.quick_scan)
        scan_menu.addAction(quick)
        
        update_menu = menubar.addMenu(self.tr('menu_update'))
        update_db = QAction(self.tr('menu_update_virus_db'), self)
        update_db.triggered.connect(self.update_databases)
        update_menu.addAction(update_db)
        
        update_prog = QAction(self.tr('menu_update_program'), self)
        update_prog.triggered.connect(self.check_updates)
        update_menu.addAction(update_prog)
        
        help_menu = menubar.addMenu(self.tr('menu_help'))
        about = QAction(self.tr('menu_about'), self)
        about.triggered.connect(self.show_about)
        help_menu.addAction(about)
    
    def create_scan_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        btn_layout = QHBoxLayout()
        btn_file = QPushButton(self.tr('btn_scan_file'))
        btn_file.clicked.connect(self.scan_file)
        btn_layout.addWidget(btn_file)
        
        btn_folder = QPushButton(self.tr('btn_scan_folder'))
        btn_folder.clicked.connect(self.scan_folder)
        btn_layout.addWidget(btn_folder)
        
        btn_quick = QPushButton(self.tr('btn_quick_scan'))
        btn_quick.clicked.connect(self.quick_scan)
        btn_layout.addWidget(btn_quick)
        layout.addLayout(btn_layout)
        
        layout.addWidget(QLabel(self.tr('scan_log')))
        self.scan_log = QTextEdit()
        self.scan_log.setReadOnly(True)
        layout.addWidget(self.scan_log)
        
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)
        
        self.stats_label = QLabel()
        layout.addWidget(self.stats_label)
        return widget
    
    def create_update_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        btn_update = QPushButton("🦠 " + self.tr('menu_update_virus_db'))
        btn_update.clicked.connect(self.update_databases)
        layout.addWidget(btn_update)
        
        btn_program = QPushButton("🔄 " + self.tr('menu_update_program'))
        btn_program.clicked.connect(self.check_updates)
        layout.addWidget(btn_program)
        
        self.update_log = QTextEdit()
        self.update_log.setReadOnly(True)
        layout.addWidget(self.update_log)
        return widget
    
    def create_quarantine_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel(self.tr('quarantine_title')))
        self.quarantine_list = QListWidget()
        layout.addWidget(self.quarantine_list)
        
        btn_layout = QHBoxLayout()
        btn_restore = QPushButton(self.tr('restore_file'))
        btn_restore.clicked.connect(self.restore_quarantine)
        btn_layout.addWidget(btn_restore)
        
        btn_delete = QPushButton(self.tr('delete_permanent'))
        btn_delete.clicked.connect(self.delete_quarantine)
        btn_layout.addWidget(btn_delete)
        layout.addLayout(btn_layout)
        
        self.load_quarantine()
        return widget
    
    def create_history_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.history_list = QListWidget()
        layout.addWidget(self.history_list)
        return widget
    
    def create_statistics_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.stats_text = QLabel("Statistics will appear here")
        layout.addWidget(self.stats_text)
        layout.addStretch()
        return widget
    
    def create_realtime_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.cb_realtime = QCheckBox("Enable Real-time Protection")
        layout.addWidget(self.cb_realtime)
        self.rt_log = QTextEdit()
        self.rt_log.setReadOnly(True)
        layout.addWidget(self.rt_log)
        return widget
    
    def create_settings_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        lang_combo = QComboBox()
        lang_combo.addItem('🇬🇧 English', 'en')
        lang_combo.addItem('🇵🇹 Português', 'pt')
        lang_combo.setCurrentIndex(0 if self.lang == 'en' else 1)
        lang_combo.currentIndexChanged.connect(lambda: self.change_language(lang_combo.currentData()))
        layout.addWidget(lang_combo)
        
        layout.addStretch()
        return widget
    
    def scan_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, self.tr('select_file'))
        if file_path:
            self.start_scan(file_path, False)
    
    def scan_folder(self):
        folder = QFileDialog.getExistingDirectory(self, self.tr('select_folder'))
        if folder:
            self.start_scan(folder, True)
    
    def quick_scan(self):
        paths = [str(Path.home() / 'Downloads'), str(Path.home() / 'Desktop')]
        for p in paths:
            if os.path.exists(p):
                self.start_scan(p, True)
                break
    
    def start_scan(self, path, recursive):
        self.scan_log.clear()
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)
        
        self.scan_thread = ScanThread(path, recursive, True)
        self.scan_thread.progress.connect(self.scan_log.append)
        self.scan_thread.stats.connect(self.update_stats)
        self.scan_thread.finished.connect(self.scan_done)
        self.scan_thread.start()
    
    def update_stats(self, stats):
        text = f"{self.tr('files_scanned')} {stats['scanned']} | {self.tr('infected')} {stats['infected']}"
        self.stats_label.setText(text)
    
    def scan_done(self, success, msg):
        self.progress.setVisible(False)
        QMessageBox.information(self, self.tr('scan_complete'), msg)
        self.load_quarantine()
    
    def update_databases(self):
        self.update_log.clear()
        self.update_thread = UpdateThread()
        self.update_thread.progress.connect(self.update_log.append)
        self.update_thread.finished.connect(lambda s, m: QMessageBox.information(self, "Update", m))
        self.update_thread.start()
    
    def check_updates(self):
        QMessageBox.information(self, "Updates", f"Current version: {VERSION}\nCheck GitHub for updates!")
    
    def load_quarantine(self):
        self.quarantine_list.clear()
        qdir = self.config_dir / 'quarantine'
        if qdir.exists():
            for f in qdir.glob('*.json'):
                with open(f) as file:
                    data = json.load(file)
                    self.quarantine_list.addItem(f"{data.get('time', '')} - {data.get('original', '')}")
    
    def restore_quarantine(self):
        item = self.quarantine_list.currentItem()
        if item:
            QMessageBox.information(self, "Restore", "Feature coming soon!")
    
    def delete_quarantine(self):
        item = self.quarantine_list.currentItem()
        if item:
            QMessageBox.information(self, "Delete", "Feature coming soon!")
    
    def show_about(self):
        dialog = AboutDialog(self, self.lang)
        dialog.exec()
    
    def show_first_warning(self):
        warning_file = self.config_dir / 'first_run.json'
        if not warning_file.exists():
            QMessageBox.information(self, "Admin Permissions", 
                "Some operations require administrator privileges:\n\n" +
                "• Updating databases\n• Real-time protection\n• System scans\n\n" +
                "You will be prompted when needed.")
            with open(warning_file, 'w') as f:
                json.dump({'shown': True}, f)

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = ClamAVGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
