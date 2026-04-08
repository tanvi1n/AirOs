import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
                             QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QFrame)
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtGui import QFont

class AppWindow(QWidget):
    def __init__(self, app_name, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.setStyleSheet("background-color: white;")
        self.resize(800, 600)
        
        # Center on screen
        screen = QApplication.desktop().screenGeometry()
        self.move((screen.width() - 800) // 2, (screen.height() - 600) // 2)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Title bar
        title_bar = QFrame()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet("background-color: #f0f0f0; border-bottom: 1px solid #ccc;")
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(15, 0, 10, 0)
        
        # App name
        title_label = QLabel(app_name)
        title_label.setStyleSheet("color: #333; font-size: 14px; font-weight: bold;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        # Close button
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(40, 30)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #666;
                font-size: 18px;
                border: none;
            }
            QPushButton:hover {
                background-color: #e81123;
                color: white;
            }
        """)
        close_btn.clicked.connect(self.close)
        title_layout.addWidget(close_btn)
        
        layout.addWidget(title_bar)
        
        # Content area
        content = QLabel(f"{app_name} is running...")
        content.setAlignment(Qt.AlignCenter)
        content.setStyleSheet("color: #666; font-size: 16px;")
        layout.addWidget(content)

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
    def __init__(self):
        super().__init__()
        self.open_windows = []
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('AirOS Desktop')
        self.showFullScreen()
        
        # Main container
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Desktop area
        desktop = QWidget()
        desktop.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #1a1a2e, stop:0.5 #16213e, stop:1 #0f3460);
        """)
        desktop_layout = QHBoxLayout(desktop)
        desktop_layout.setContentsMargins(30, 30, 30, 30)
        desktop_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        # Desktop icons in vertical columns
        icons_layout = QGridLayout()
        icons_layout.setSpacing(20)
        icons_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        # Create desktop icons
        apps = [
            ("🌐", "Browser"),
            ("📁", "Files"),
            ("⚙️", "Settings"),
            ("📧", "Mail"),
            ("🎵", "Music"),
            ("📷", "Camera"),
            ("📝", "Notes"),
            ("🎮", "Games")
        ]
        
        # Arrange in vertical columns (like real desktop)
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
        
        main_layout.addWidget(desktop)
        
        # Taskbar
        taskbar = QFrame()
        taskbar.setFixedHeight(50)
        taskbar.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0.85);
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        """)
        taskbar_layout = QHBoxLayout(taskbar)
        taskbar_layout.setContentsMargins(15, 0, 15, 0)
        
        taskbar_layout.addStretch()
        
        # System tray
        tray_layout = QHBoxLayout()
        tray_layout.setSpacing(15)
        
        # WiFi icon
        wifi = QLabel("📶")
        wifi.setStyleSheet("color: white; font-size: 18px;")
        tray_layout.addWidget(wifi)
        
        # Volume icon
        volume = QLabel("🔊")
        volume.setStyleSheet("color: white; font-size: 18px;")
        tray_layout.addWidget(volume)
        
        # Clock
        self.clock = QLabel()
        self.clock.setStyleSheet("color: white; font-size: 14px; padding: 5px;")
        self.update_clock()
        tray_layout.addWidget(self.clock)
        
        # Timer for clock
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
        window = AppWindow(app_name, self)
        window.show()
        self.open_windows.append(window)
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = DesktopUI()
    sys.exit(app.exec_())
