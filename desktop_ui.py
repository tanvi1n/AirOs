import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
                             QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QFrame, QTextEdit, QComboBox)
from PyQt5.QtCore import Qt, QTimer, QTime, pyqtSignal
from PyQt5.QtGui import QFont
from realistic_apps import DocumentViewer, PowerPointWindow

class BrowserWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: white;")
        self.resize(900, 650)
        
        screen = QApplication.desktop().screenGeometry()
        self.move((screen.width() - 900) // 2, (screen.height() - 650) // 2)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        title_bar = self.create_title_bar("Browser")
        layout.addWidget(title_bar)
        
        addr_bar = QFrame()
        addr_bar.setFixedHeight(50)
        addr_bar.setStyleSheet("background-color: #f5f5f5; border-bottom: 1px solid #ddd;")
        addr_layout = QHBoxLayout(addr_bar)
        addr_layout.setContentsMargins(10, 10, 10, 10)
        
        url_input = QLabel("🔒 https://airos-demo.local")
        url_input.setStyleSheet("background-color: white; padding: 8px; border-radius: 5px; border: 1px solid #ccc;")
        addr_layout.addWidget(url_input)
        layout.addWidget(addr_bar)
        
        content = QLabel("Welcome to AirOS Browser\n\n🌐 Gesture-controlled browsing")
        content.setAlignment(Qt.AlignCenter)
        content.setStyleSheet("font-size: 18px; color: #666;")
        layout.addWidget(content)
    
    def create_title_bar(self, title):
        title_bar = QFrame()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet("background-color: #f0f0f0; border-bottom: 1px solid #ccc;")
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(15, 0, 10, 0)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #333; font-size: 14px; font-weight: bold;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(40, 30)
        close_btn.setStyleSheet("""
            QPushButton { background-color: transparent; color: #666; font-size: 18px; border: none; }
            QPushButton:hover { background-color: #e81123; color: white; }
        """)
        close_btn.clicked.connect(self.close)
        title_layout.addWidget(close_btn)
        
        return title_bar

class FilesWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: white;")
        self.resize(800, 600)
        
        screen = QApplication.desktop().screenGeometry()
        self.move((screen.width() - 800) // 2, (screen.height() - 600) // 2)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        title_bar = self.create_title_bar("Files")
        self.main_layout.addWidget(title_bar)
        
        # Navigation bar
        nav_bar = QFrame()
        nav_bar.setFixedHeight(40)
        nav_bar.setStyleSheet("background-color: #f5f5f5; border-bottom: 1px solid #ddd;")
        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setContentsMargins(10, 5, 10, 5)
        
        self.back_btn = QPushButton("← Back")
        self.back_btn.setStyleSheet("background-color: transparent; border: none; font-size: 13px;")
        self.back_btn.clicked.connect(self.go_back)
        self.back_btn.setEnabled(False)
        nav_layout.addWidget(self.back_btn)
        
        self.path_label = QLabel("📁 Home")
        self.path_label.setStyleSheet("font-size: 13px; color: #666;")
        nav_layout.addWidget(self.path_label)
        nav_layout.addStretch()
        
        self.main_layout.addWidget(nav_bar)
        
        # Content area
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.content_layout.setAlignment(Qt.AlignTop)
        
        self.main_layout.addWidget(self.content_area)
        
        self.current_folder = None
        self.show_folders()
    
    def show_folders(self):
        self.clear_content()
        self.current_folder = None
        self.back_btn.setEnabled(False)
        self.path_label.setText("📁 Home")
        
        folders = ["📁 Documents", "📁 Downloads", "📁 Pictures", "📁 Videos", "📁 Music"]
        for folder in folders:
            folder_btn = QPushButton(folder)
            folder_btn.setFixedHeight(40)
            folder_btn.setStyleSheet("""
                QPushButton { text-align: left; padding-left: 15px; background-color: #f9f9f9; 
                             border: 1px solid #e0e0e0; font-size: 14px; }
                QPushButton:hover { background-color: #e8f4fd; }
            """)
            folder_btn.clicked.connect(lambda checked, f=folder: self.open_folder(f))
            self.content_layout.addWidget(folder_btn)
    
    def open_folder(self, folder_name):
        self.clear_content()
        self.current_folder = folder_name
        self.back_btn.setEnabled(True)
        self.path_label.setText(f"📁 Home > {folder_name}")
        
        # Sample files for each folder (more files for scrolling demo)
        files = {
            "📁 Documents": [
                "📄 Project Report.docx", "📄 Resume.pdf", "📄 Notes.txt",
                "📄 Meeting Minutes.docx", "📄 Budget 2026.xlsx", "📄 Presentation.pptx",
                "📄 Contract.pdf", "📄 Invoice.pdf", "📄 Letter.docx",
                "📄 Research Paper.pdf", "📄 Thesis.docx", "📄 Assignment.pdf",
                "📄 Proposal.docx", "📄 Report Q1.xlsx", "📄 Analysis.pdf",
                "📄 Summary.txt", "📄 Guidelines.pdf", "📄 Manual.pdf"
            ],
            "📁 Downloads": [
                "📦 installer.exe", "📄 document.pdf", "🖼️ image.jpg",
                "📦 setup.msi", "📄 ebook.pdf", "🖼️ wallpaper.png",
                "📦 software.zip", "📄 guide.pdf", "🖼️ photo.jpg",
                "📦 update.exe", "📄 manual.pdf", "🖼️ screenshot.png",
                "📦 driver.exe", "📄 readme.txt", "🖼️ banner.jpg"
            ],
            "📁 Pictures": [
                "🖼️ vacation_2025.jpg", "🖼️ family_photo.png", "🖼️ screenshot_01.png",
                "🖼️ birthday_party.jpg", "🖼️ sunset.jpg", "🖼️ landscape.png",
                "🖼️ portrait.jpg", "🖼️ nature.jpg", "🖼️ city_view.png",
                "🖼️ beach.jpg", "🖼️ mountains.jpg", "🖼️ friends.png",
                "🖼️ wedding.jpg", "🖼️ graduation.jpg", "🖼️ travel.png"
            ],
            "📁 Videos": [
                "🎬 tutorial_part1.mp4", "🎬 movie_2025.avi", "🎬 clip_01.mov",
                "🎬 tutorial_part2.mp4", "🎬 presentation.mp4", "🎬 demo.avi",
                "🎬 recording.mov", "🎬 webinar.mp4", "🎬 lecture.avi",
                "🎬 vlog.mp4", "🎬 interview.mov", "🎬 gameplay.mp4"
            ],
            "📁 Music": [
                "🎵 favorite_song.mp3", "🎵 playlist_01.mp3", "🎵 album_track1.flac",
                "🎵 rock_song.mp3", "🎵 jazz_music.mp3", "🎵 classical.flac",
                "🎵 pop_hit.mp3", "🎵 indie_track.mp3", "🎵 electronic.mp3",
                "🎵 acoustic.mp3", "🎵 remix.mp3", "🎵 cover.mp3",
                "🎵 instrumental.flac", "🎵 live_recording.mp3", "🎵 podcast.mp3"
            ]
        }
        
        folder_files = files.get(folder_name, ["📄 Empty folder"])
        
        for file in folder_files:
            file_btn = QPushButton(file)
            file_btn.setFixedHeight(35)
            file_btn.setStyleSheet("""
                QPushButton { text-align: left; padding-left: 20px; background-color: white; 
                             border-bottom: 1px solid #f0f0f0; font-size: 13px; }
                QPushButton:hover { background-color: #f9f9f9; }
            """)
            file_btn.clicked.connect(lambda checked, f=file: self.open_file(f))
            self.content_layout.addWidget(file_btn)
    
    def open_file(self, file_name):
        print(f"Opening: {file_name}")
    
    def go_back(self):
        self.show_folders()
    
    def clear_content(self):
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    def create_title_bar(self, title):
        title_bar = QFrame()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet("background-color: #f0f0f0; border-bottom: 1px solid #ccc;")
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(15, 0, 10, 0)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #333; font-size: 14px; font-weight: bold;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(40, 30)
        close_btn.setStyleSheet("""
            QPushButton { background-color: transparent; color: #666; font-size: 18px; border: none; }
            QPushButton:hover { background-color: #e81123; color: white; }
        """)
        close_btn.clicked.connect(self.close)
        title_layout.addWidget(close_btn)
        
        return title_bar

class NotesWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: white;")
        self.resize(700, 500)
        
        screen = QApplication.desktop().screenGeometry()
        self.move((screen.width() - 700) // 2, (screen.height() - 500) // 2)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        title_bar = self.create_title_bar("Notes")
        layout.addWidget(title_bar)
        
        text_area = QTextEdit()
        text_area.setPlaceholderText("Start typing your notes here...")
        text_area.setStyleSheet("font-size: 14px; padding: 15px; border: none;")
        layout.addWidget(text_area)
    
    def create_title_bar(self, title):
        title_bar = QFrame()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet("background-color: #f0f0f0; border-bottom: 1px solid #ccc;")
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(15, 0, 10, 0)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #333; font-size: 14px; font-weight: bold;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(40, 30)
        close_btn.setStyleSheet("""
            QPushButton { background-color: transparent; color: #666; font-size: 18px; border: none; }
            QPushButton:hover { background-color: #e81123; color: white; }
        """)
        close_btn.clicked.connect(self.close)
        title_layout.addWidget(close_btn)
        
        return title_bar

class SettingsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: white;")
        self.resize(600, 500)
        
        screen = QApplication.desktop().screenGeometry()
        self.move((screen.width() - 600) // 2, (screen.height() - 500) // 2)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        title_bar = self.create_title_bar("Settings")
        layout.addWidget(title_bar)
        
        settings_area = QWidget()
        settings_layout = QVBoxLayout(settings_area)
        settings_layout.setContentsMargins(20, 20, 20, 20)
        settings_layout.setAlignment(Qt.AlignTop)
        
        options = ["⚙️ General", "🎨 Appearance", "🖱️ Gesture Sensitivity", "📷 Camera Settings", "ℹ️ About AirOS"]
        for option in options:
            opt_btn = QPushButton(option)
            opt_btn.setFixedHeight(50)
            opt_btn.setStyleSheet("""
                QPushButton { text-align: left; padding-left: 20px; background-color: white; 
                             border-bottom: 1px solid #e0e0e0; font-size: 14px; }
                QPushButton:hover { background-color: #f5f5f5; }
            """)
            settings_layout.addWidget(opt_btn)
        
        layout.addWidget(settings_area)
    
    def create_title_bar(self, title):
        title_bar = QFrame()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet("background-color: #f0f0f0; border-bottom: 1px solid #ccc;")
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(15, 0, 10, 0)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #333; font-size: 14px; font-weight: bold;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(40, 30)
        close_btn.setStyleSheet("""
            QPushButton { background-color: transparent; color: #666; font-size: 18px; border: none; }
            QPushButton:hover { background-color: #e81123; color: white; }
        """)
        close_btn.clicked.connect(self.close)
        title_layout.addWidget(close_btn)
        
        return title_bar

class AppWindow(QWidget):
    def __init__(self, app_name, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: white;")
        self.resize(600, 450)
        
        screen = QApplication.desktop().screenGeometry()
        self.move((screen.width() - 600) // 2, (screen.height() - 450) // 2)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        title_bar = self.create_title_bar(app_name)
        layout.addWidget(title_bar)
        
        content = QLabel(f"{app_name}\n\nComing soon...")
        content.setAlignment(Qt.AlignCenter)
        content.setStyleSheet("color: #666; font-size: 16px;")
        layout.addWidget(content)
    
    def create_title_bar(self, title):
        title_bar = QFrame()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet("background-color: #f0f0f0; border-bottom: 1px solid #ccc;")
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(15, 0, 10, 0)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #333; font-size: 14px; font-weight: bold;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(40, 30)
        close_btn.setStyleSheet("""
            QPushButton { background-color: transparent; color: #666; font-size: 18px; border: none; }
            QPushButton:hover { background-color: #e81123; color: white; }
        """)
        close_btn.clicked.connect(self.close)
        title_layout.addWidget(close_btn)
        
        return title_bar

class DesktopIcon(QPushButton):
    def __init__(self, icon, name, parent=None):
        super().__init__(parent)
        self.setText(f"{icon}\n{name}")
        self.setFixedSize(100, 100)
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                font-size: 12px;
                border: none;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.15);
                border-radius: 8px;
            }
        """)

class DesktopUI(QMainWindow):
    recalibrate_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.open_windows = []
        self.current_mode = 'desktop'
        self.current_gesture = 'None'
        self.fps = 0
        self.hand_detected = False
        self.esc_count = 0
        self.esc_timer = None
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('AirOS Desktop')
        self.showFullScreen()
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        desktop = QWidget()
        desktop.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #1a1a2e, stop:0.5 #16213e, stop:1 #0f3460);
        """)
        desktop_layout = QHBoxLayout(desktop)
        desktop_layout.setContentsMargins(30, 30, 30, 30)
        desktop_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        icons_layout = QGridLayout()
        icons_layout.setSpacing(20)
        icons_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        apps = [
       ("🌐", "Browser"),
    ("📁", "Files"),
    ("📄", "Document"),
    ("📊", "Presentation"),
    ("⚙️", "Settings"),
    ("📝", "Notes"),
    ("📧", "Mail"),
    ("🎵", "Music")
]
        
        row, col = 0, 0
        max_rows = 4
        for icon, name in apps:
            btn = DesktopIcon(icon, name)
            btn.clicked.connect(lambda checked, n=name: self.open_app(n))
            icons_layout.addWidget(btn, row, col)
            row += 1
            if row >= max_rows:
                row = 0
                col += 1
        
        desktop_layout.addLayout(icons_layout)
        desktop_layout.addStretch()
        
        # Stats panel
        self.stats_panel = QLabel()
        self.stats_panel.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0.8);
            color: #00ff00;
            padding: 15px;
            border-radius: 10px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            border: 2px solid rgba(0, 255, 0, 0.3);
        """)
        self.stats_panel.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.stats_panel.setFixedSize(220, 140)
        self.stats_panel.setParent(desktop)
        self.stats_panel.move(self.width() - 240, 20)
        self.stats_panel.raise_()
        self.update_stats()
        
        main_layout.addWidget(desktop)
        
        taskbar = QFrame()
        taskbar.setFixedHeight(50)
        taskbar.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0.85);
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        """)
        taskbar_layout = QHBoxLayout(taskbar)
        taskbar_layout.setContentsMargins(15, 0, 15, 0)
        
        # Mode selector
        self.mode_selector = QComboBox()
        self.mode_selector.addItems(['Desktop', 'Document', 'Presentation', 'Browser'])
        self.mode_selector.setStyleSheet("""
            QComboBox {
                background-color: rgba(255,255,255,0.1);
                color: white;
                padding: 5px 15px;
                border-radius: 5px;
                font-size: 13px;
                min-width: 120px;
            }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView {
                background-color: #2c3e50;
                color: white;
                selection-background-color: #3498db;
            }
        """)
        taskbar_layout.addWidget(self.mode_selector)
        
        taskbar_layout.addStretch()
        
        tray_layout = QHBoxLayout()
        tray_layout.setSpacing(15)
        
        wifi = QLabel("📶")
        wifi.setStyleSheet("color: white; font-size: 18px;")
        tray_layout.addWidget(wifi)
        
        volume = QLabel("🔊")
        volume.setStyleSheet("color: white; font-size: 18px;")
        tray_layout.addWidget(volume)
        
        self.clock = QLabel()
        self.clock.setStyleSheet("color: white; font-size: 14px; padding: 5px;")
        self.update_clock()
        tray_layout.addWidget(self.clock)
        
        timer = QTimer(self)
        timer.timeout.connect(self.update_clock)
        timer.start(1000)
        
        taskbar_layout.addLayout(tray_layout)
        main_layout.addWidget(taskbar)
    
    def update_clock(self):
        current_time = QTime.currentTime()
        self.clock.setText(current_time.toString('hh:mm:ss'))
        
    def open_app(self, app_name):
        print(f"✓ Opening {app_name}...")

        if app_name == "Browser":
            window = BrowserWindow(self)
            self.mode_selector.setCurrentIndex(3)  # Auto-switch to Browser
            print("🔄 Auto-switched to Browser mode")
        elif app_name == "Files":
            window = FilesWindow(self)
            self.mode_selector.setCurrentIndex(0)  # Desktop
        elif app_name == "Notes":
            window = NotesWindow(self)
            self.mode_selector.setCurrentIndex(0)  # Desktop
        elif app_name == "Settings":
            window = SettingsWindow(self)
            self.mode_selector.setCurrentIndex(0)  # Desktop
        elif app_name == "Document":
            window = DocumentViewer(self)
            self.mode_selector.setCurrentIndex(1)  # Document mode
            print("🔄 Auto-switched to Document mode")
        elif app_name == "Presentation":
            window = PowerPointWindow(self)
            self.mode_selector.setCurrentIndex(2)  # Presentation mode  # Auto-switch to Presentation
            print("🔄 Auto-switched to Presentation mode")
        else:
            window = AppWindow(app_name, self)
            self.mode_selector.setCurrentIndex(0)  # Desktop

        window.show()
        self.open_windows.append(window)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.esc_count += 1
            print(f"⚠ ESC pressed {self.esc_count}/3 times (press 3 times to exit)")
            
            # Reset counter after 2 seconds if not pressed again
            if self.esc_timer:
                self.esc_timer.stop()
            self.esc_timer = QTimer()
            self.esc_timer.setSingleShot(True)
            self.esc_timer.timeout.connect(lambda: setattr(self, 'esc_count', 0))
            self.esc_timer.start(2000)
            
            if self.esc_count >= 3:
                print("🛑 Exiting AirOS...")
                self.close()
        elif event.key() == Qt.Key_C:
            self.recalibrate_requested.emit()
        elif event.key() == Qt.Key_1:
            self.mode_selector.setCurrentIndex(0)  # Desktop
            print("⌨ Switched to Desktop mode")
        elif event.key() == Qt.Key_2:
            self.mode_selector.setCurrentIndex(1)  # Presentation
            print("⌨ Switched to Presentation mode")
        elif event.key() == Qt.Key_3:
            self.mode_selector.setCurrentIndex(2)  # Browser
            print("⌨ Switched to Browser mode")

    def update_stats(self):
        hand_status = "✓ Detected" if self.hand_detected else "✗ No Hand"
        stats_text = f"""╔══════════════════╗
║   AIROS STATS    ║
╚══════════════════╝

FPS:      {self.fps}
Mode:     {self.current_mode.upper()}
Gesture:  {self.current_gesture}
Hand:     {hand_status}
"""
        self.stats_panel.setText(stats_text)

    def set_fps(self, fps):
        self.fps = fps
        self.update_stats()

    def set_gesture(self, gesture_name):
        self.current_gesture = gesture_name
        self.update_stats()

    def set_hand_status(self, detected):
        self.hand_detected = detected
        self.update_stats()

    def set_mode_display(self, mode):
        self.current_mode = mode
        self.update_stats()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = DesktopUI()
    sys.exit(app.exec_())
