from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QMessageBox, QDialog
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from calibration import CalibrationScreen

class UserSelectionScreen(QDialog):
    user_selected = pyqtSignal(str, dict)  # user_name, calibration_data
    
    def __init__(self):
        super().__init__()
        self.selected_user = None
        self.calibration_data = None
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('AirOS - User Selection')
        self.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1a1a2e, stop:1 #16213e);")
        self.resize(500, 600)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Title
        title = QLabel("🖐️ Welcome to AirOS")
        title.setStyleSheet("color: white; font-size: 36px; font-weight: bold; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Select User Profile")
        subtitle.setStyleSheet("color: #95a5a6; font-size: 16px; margin-bottom: 30px;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        # Get existing users
        users = CalibrationScreen.get_available_users()
        
        if users:
            # Show existing users
            users_label = QLabel("Existing Users:")
            users_label.setStyleSheet("color: white; font-size: 14px; margin-bottom: 10px;")
            layout.addWidget(users_label)
            
            for i, user in enumerate(users, 1):
                btn = QPushButton(f"{i}. {user.title()}")
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: rgba(52, 152, 219, 0.3);
                        color: white;
                        font-size: 16px;
                        padding: 15px;
                        border-radius: 8px;
                        border: 2px solid rgba(52, 152, 219, 0.5);
                        text-align: left;
                        margin: 5px;
                    }
                    QPushButton:hover {
                        background-color: rgba(52, 152, 219, 0.5);
                        border: 2px solid #3498db;
                    }
                """)
                btn.clicked.connect(lambda checked, u=user: self.select_existing_user(u))
                layout.addWidget(btn)
            
            layout.addSpacing(20)
        
        # New user section
        new_user_label = QLabel("New User:")
        new_user_label.setStyleSheet("color: white; font-size: 14px; margin-bottom: 10px;")
        layout.addWidget(new_user_label)
        
        # Name input
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name...")
        self.name_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                font-size: 16px;
                padding: 12px;
                border-radius: 8px;
                border: 2px solid rgba(255, 255, 255, 0.3);
            }
            QLineEdit:focus {
                border: 2px solid #2ecc71;
            }
        """)
        self.name_input.returnPressed.connect(self.create_new_user)
        layout.addWidget(self.name_input)
        
        # New user button
        new_btn = QPushButton("Create New Profile & Calibrate")
        new_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                font-size: 16px;
                padding: 15px;
                border-radius: 8px;
                border: none;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        new_btn.clicked.connect(self.create_new_user)
        layout.addWidget(new_btn)
        
        layout.addSpacing(20)
        
        # Default/Skip button
        skip_btn = QPushButton("Skip Calibration (Use Defaults)")
        skip_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(149, 165, 166, 0.3);
                color: white;
                font-size: 14px;
                padding: 12px;
                border-radius: 8px;
                border: 2px solid rgba(149, 165, 166, 0.5);
            }
            QPushButton:hover {
                background-color: rgba(149, 165, 166, 0.5);
            }
        """)
        skip_btn.clicked.connect(self.skip_calibration)
        layout.addWidget(skip_btn)
        
        layout.addStretch()
        
        # Keyboard shortcuts hint
        hint = QLabel("Tip: Press number keys (1-9) or type name and press Enter")
        hint.setStyleSheet("color: #7f8c8d; font-size: 12px; margin-top: 10px;")
        hint.setAlignment(Qt.AlignCenter)
        layout.addWidget(hint)
    
    def select_existing_user(self, user_name):
        """Load existing user's calibration"""
        self.selected_user = user_name
        self.calibration_data = CalibrationScreen.load_calibration(user_name)
        print(f"✓ Loaded profile: {user_name}")
        self.user_selected.emit(user_name, self.calibration_data)
        self.close()
    
    def create_new_user(self):
        """Create new user and run calibration"""
        name = self.name_input.text().strip().lower()
        
        if not name:
            QMessageBox.warning(self, "Name Required", "Please enter your name.")
            return
        
        if not name.replace('_', '').isalnum():
            QMessageBox.warning(self, "Invalid Name", "Name can only contain letters, numbers, and underscores.")
            return
        
        self.selected_user = name
        print(f"✓ Creating new profile: {name}")
        
        # Run calibration
        self.hide()
        calibration = CalibrationScreen(user_name=name)
        calibration.show()
        calibration.exec_()
        
        # Get calibration data
        self.calibration_data = calibration.get_calibration_data()
        self.user_selected.emit(name, self.calibration_data)
        self.close()
    
    def skip_calibration(self):
        """Skip calibration and use defaults"""
        self.selected_user = "default"
        self.calibration_data = {
            'pinch_threshold': 30,
            'swipe_threshold': 0.15,
            'user_name': 'default'
        }
        print("⚠ Using default calibration")
        self.user_selected.emit("default", self.calibration_data)
        self.close()
    
    def keyPressEvent(self, event):
        """Handle keyboard shortcuts"""
        key = event.text()
        
        # Number keys for quick selection
        if key.isdigit():
            users = CalibrationScreen.get_available_users()
            index = int(key) - 1
            if 0 <= index < len(users):
                self.select_existing_user(users[index])
        
        # 'n' for new user
        elif key.lower() == 'n':
            self.name_input.setFocus()
        
        # 'd' for default
        elif key.lower() == 'd':
            self.skip_calibration()
