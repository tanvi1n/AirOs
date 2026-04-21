import cv2
import math
import json
import os
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QDialog
from PyQt5.QtCore import Qt, QTimer
from hand_tracking import HandTracker

class CalibrationScreen(QDialog):
    def __init__(self, user_name=None):
        super().__init__()
        self.user_name = user_name
        self.tracker = HandTracker()
        self.calibration_data = {
            'pinch_threshold': 30,
            'swipe_threshold': 0.15,
            'user_name': user_name
        }
        self.pinch_measurements = []
        self.swipe_measurements = []
        self.hand_x_positions = []
        self.step = 0
        self.cap = None
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('AirOS Calibration')
        self.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2c3e50, stop:1 #3498db);")
        self.resize(600, 400)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        title = QLabel("🖐️ AirOS Calibration")
        title.setStyleSheet("color: white; font-size: 32px; font-weight: bold; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        self.instruction = QLabel()
        self.instruction.setStyleSheet("color: white; font-size: 18px; margin: 20px; padding: 20px;")
        self.instruction.setAlignment(Qt.AlignCenter)
        self.instruction.setWordWrap(True)
        layout.addWidget(self.instruction)
        
        self.status = QLabel()
        self.status.setStyleSheet("color: #2ecc71; font-size: 16px; margin: 10px;")
        self.status.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status)
        
        self.start_btn = QPushButton("Start Calibration")
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                font-size: 16px;
                padding: 15px 40px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        self.start_btn.clicked.connect(self.start_calibration)
        layout.addWidget(self.start_btn, alignment=Qt.AlignCenter)
        
        self.update_instruction()
        
    def update_instruction(self):
        if self.step == 0:
            self.instruction.setText("Welcome! We'll calibrate the system to your hand.\n\nThis takes about 15 seconds.")
            self.status.setText("")
        elif self.step == 1:
            self.instruction.setText("Step 1/3: Show your open hand to the camera")
            self.status.setText("Detecting hand...")
        elif self.step == 2:
            self.instruction.setText("Step 2/3: Make a pinch gesture 3 times\n(Bring thumb and index finger together)")
            self.status.setText(f"Pinches detected: {len(self.pinch_measurements)}/3")
        elif self.step == 3:
            self.instruction.setText("Step 3/3: Point your THUMB to the LEFT\n(Keep index finger pointing forward)")
            self.status.setText("Waiting for thumb left...")
        elif self.step == 4:
            self.instruction.setText("Step 3/3: Now point your THUMB to the RIGHT\n(Keep index finger pointing forward)")
            self.status.setText("Waiting for thumb right...")
        elif self.step == 5:
            self.instruction.setText("✓ Calibration Complete!\n\nStarting AirOS...")
            self.status.setText("Ready to go!")
    
    def start_calibration(self):
        self.start_btn.hide()
        self.step = 1
        self.update_instruction()
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        QTimer.singleShot(100, self.calibration_loop)
    
    def calibration_loop(self):
        if self.step == 1:
            self.calibrate_hand_detection()
        elif self.step == 2:
            self.calibrate_pinch()
        elif self.step == 3:
            self.calibrate_swipe_left()
        elif self.step == 4:
            self.calibrate_swipe_right()
        elif self.step == 5:
            self.finish_calibration()
    
    def calibrate_hand_detection(self):
        ret, frame = self.cap.read()
        if not ret:
            QTimer.singleShot(100, self.calibration_loop)
            return
        
        frame = cv2.flip(frame, 1)
        landmarks = self.tracker.extract_landmarks(frame)
        
        cv2.putText(frame, "Show your open hand", (150, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Calibration', frame)
        cv2.waitKey(1)
        
        if landmarks:
            self.status.setText("✓ Hand detected!")
            self.step = 2
            self.update_instruction()
            QTimer.singleShot(1000, self.calibration_loop)
        else:
            QTimer.singleShot(100, self.calibration_loop)
    
    def calibrate_pinch(self):
        ret, frame = self.cap.read()
        if not ret:
            QTimer.singleShot(100, self.calibration_loop)
            return
        
        frame = cv2.flip(frame, 1)
        landmarks = self.tracker.extract_landmarks(frame)
        
        cv2.putText(frame, f"Pinch {len(self.pinch_measurements)}/3", (200, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Calibration', frame)
        cv2.waitKey(1)
        
        if landmarks:
            index_tip = landmarks['index_tip']
            thumb_tip = landmarks['thumb_tip']
            
            distance = math.sqrt(
                (thumb_tip[0] - index_tip[0])**2 + 
                (thumb_tip[1] - index_tip[1])**2
            )
            
            if distance < 40 and len(self.pinch_measurements) < 3:
                self.pinch_measurements.append(distance)
                self.status.setText(f"✓ Pinch {len(self.pinch_measurements)}/3 recorded!")
                self.update_instruction()
                
                if len(self.pinch_measurements) >= 3:
                    avg_pinch = sum(self.pinch_measurements) / len(self.pinch_measurements)
                    self.calibration_data['pinch_threshold'] = int(avg_pinch * 1.3)
                    self.step = 3
                    self.update_instruction()
                    QTimer.singleShot(2000, self.calibration_loop)  # 2 sec before next step
                    return
                
                QTimer.singleShot(2000, self.calibration_loop)  # 2 sec between pinches
                return
        
        QTimer.singleShot(100, self.calibration_loop)
    
    def calibrate_swipe_left(self):
        ret, frame = self.cap.read()
        if not ret:
            QTimer.singleShot(100, self.calibration_loop)
            return
        
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        landmarks = self.tracker.extract_landmarks(frame)
        
        cv2.putText(frame, "Point THUMB LEFT (or SPACE to skip)", (100, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, "Keep index forward, move thumb left", (100, 90), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        
        if landmarks:
            index_tip = landmarks['index_tip']
            thumb_tip = landmarks['thumb_tip']
            horizontal_diff = thumb_tip[0] - index_tip[0]
            
            # Show live distance feedback
            cv2.putText(frame, f"Distance: {int(abs(horizontal_diff))} px (need 50+)", (100, 130), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        cv2.imshow('Calibration', frame)
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord(' '):
            self.swipe_measurements.append(80)
            self.status.setText("⚠ Skipped - using default")
            self.step = 4
            self.update_instruction()
            QTimer.singleShot(1000, self.calibration_loop)
            return
        
        if landmarks:
            # Thumb is LEFT of index (negative difference, need at least 50px)
            if horizontal_diff < -50:
                self.swipe_measurements.append(abs(horizontal_diff))
                self.status.setText(f"✓ Thumb left detected! ({int(abs(horizontal_diff))}px)")
                self.step = 4
                self.update_instruction()
                QTimer.singleShot(2000, self.calibration_loop)
                return
        
        QTimer.singleShot(100, self.calibration_loop)
    
    def calibrate_swipe_right(self):
        ret, frame = self.cap.read()
        if not ret:
            QTimer.singleShot(100, self.calibration_loop)
            return
        
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        landmarks = self.tracker.extract_landmarks(frame)
        
        cv2.putText(frame, "Point THUMB RIGHT (or SPACE to skip)", (100, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, "Keep index forward, move thumb right", (100, 90),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        
        if landmarks:
            index_tip = landmarks['index_tip']
            thumb_tip = landmarks['thumb_tip']
            horizontal_diff = thumb_tip[0] - index_tip[0]
            
            # Show live distance feedback
            cv2.putText(frame, f"Distance: {int(abs(horizontal_diff))} px (need 50+)", (100, 130),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        cv2.imshow('Calibration', frame)
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord(' '):
            self.swipe_measurements.append(80)
            avg_threshold = sum(self.swipe_measurements) / len(self.swipe_measurements)
            self.calibration_data['swipe_threshold'] = int(avg_threshold)
            self.status.setText("⚠ Skipped - using default")
            self.step = 5
            self.update_instruction()
            QTimer.singleShot(1000, self.calibration_loop)
            return
        
        if landmarks:
            # Thumb is RIGHT of index (positive difference, need at least 50px)
            if horizontal_diff > 50:
                self.swipe_measurements.append(abs(horizontal_diff))
                avg_threshold = sum(self.swipe_measurements) / len(self.swipe_measurements)
                self.calibration_data['swipe_threshold'] = int(avg_threshold * 0.8)
                self.status.setText(f"✓ Thumb right detected! ({int(abs(horizontal_diff))}px)")
                self.step = 5
                self.update_instruction()
                QTimer.singleShot(2000, self.calibration_loop)
                return
        
        QTimer.singleShot(100, self.calibration_loop)
    
    def finish_calibration(self):
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        
        # Save calibration
        self.save_calibration()
        print(f"✓ Calibration complete: {self.calibration_data}")
        QTimer.singleShot(1000, self.close)
    
    def save_calibration(self):
        """Save calibration data to JSON file"""
        os.makedirs('calibrations', exist_ok=True)
        filename = f"calibrations/{self.user_name}.json"
        with open(filename, 'w') as f:
            json.dump(self.calibration_data, f, indent=2)
        print(f"✓ Saved calibration to {filename}")
    
    @staticmethod
    def load_calibration(user_name):
        """Load calibration data from JSON file"""
        filename = f"calibrations/{user_name}.json"
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return json.load(f)
        return None
    
    @staticmethod
    def get_available_users():
        """Get list of calibrated users"""
        if not os.path.exists('calibrations'):
            return []
        files = os.listdir('calibrations')
        users = [f.replace('.json', '') for f in files if f.endswith('.json')]
        return users
    
    def get_calibration_data(self):
        return self.calibration_data
