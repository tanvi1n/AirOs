import sys
import cv2
import math
import time
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal
from hand_tracking import HandTracker
from gesture_control import GestureController
from desktop_ui import DesktopUI
from user_selection import UserSelectionScreen
from calibration import CalibrationScreen

class HandTrackingThread(QThread):
    """Thread to run hand tracking without blocking UI"""
    gesture_detected = pyqtSignal(float, float, float)
    fps_updated = pyqtSignal(int)
    gesture_name_updated = pyqtSignal(str)
    hand_status_updated = pyqtSignal(bool)
    
    def __init__(self):
        super().__init__()
        self.tracker = HandTracker()
        self.running = True
        self.paused = False
        self.frame_count = 0
        self.start_time = time.time()
        self.last_thumb_pos = None
        self.last_index_pos = None
        self.last_landmarks = None
        
    def run(self):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)
        
        while self.running and cap.isOpened():
            if self.paused:
                time.sleep(0.1)
                continue
            
            ret, frame = cap.read()
            if not ret:
                continue
            
            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            
            landmarks = self.tracker.extract_landmarks(frame)
            
            if landmarks:
                self.hand_status_updated.emit(True)
                index_tip = landmarks['index_tip']
                thumb_tip = landmarks['thumb_tip']
                
                # Normalize coordinates (0-1 range)
                x = index_tip[0] / w
                y = index_tip[1] / h
                
                # Calculate distance between thumb and index
                distance = math.sqrt(
                    (thumb_tip[0] - index_tip[0])**2 + 
                    (thumb_tip[1] - index_tip[1])**2
                )
                
                # Emit gesture data with thumb and index positions
                self.gesture_detected.emit(x, y, distance)
                
                # Store positions for gesture controller
                self.last_thumb_pos = thumb_tip
                self.last_index_pos = index_tip
                self.last_landmarks = landmarks 

                # Visual feedback
                cv2.circle(frame, index_tip, 8, (0, 255, 0), -1)
                cv2.circle(frame, thumb_tip, 8, (255, 0, 0), -1)
            else:
                self.hand_status_updated.emit(False)
            
            # Calculate FPS
            self.frame_count += 1
            if self.frame_count % 30 == 0:
                elapsed = time.time() - self.start_time
                fps = int(30 / elapsed) if elapsed > 0 else 0
                self.fps_updated.emit(fps)
                self.start_time = time.time()
            
            cv2.imshow('AirOS - Hand Tracking (Q=quit, C=recalibrate)', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                self.running = False
                break
        
        cap.release()
        cv2.destroyAllWindows()
    
    def pause(self):
        self.paused = True
    
    def resume(self):
        self.paused = False
    
    def stop(self):
        self.running = False

class AirOS:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.current_user = None
        self.calibration_data = None
        
        # Show user selection first
        self.show_user_selection()
        
    def show_user_selection(self):
        """Show user selection screen"""
        user_screen = UserSelectionScreen()
        user_screen.user_selected.connect(self.on_user_selected)
        user_screen.show()
        user_screen.exec_()
    
    def on_user_selected(self, user_name, calibration_data):
        """Called when user is selected"""
        self.current_user = user_name
        self.calibration_data = calibration_data
        print(f"✓ User: {user_name}")
        print(f"✓ Calibration: {calibration_data}")
        
        # Initialize system components
        self.ui = DesktopUI()
        self.controller = GestureController()
        self.tracking_thread = HandTrackingThread()
        
        # Apply calibration
        self.controller.set_calibration(calibration_data)
        
        # Connect signals
        self.tracking_thread.gesture_detected.connect(self.handle_gesture)
        self.tracking_thread.fps_updated.connect(self.ui.set_fps)
        self.tracking_thread.gesture_name_updated.connect(self.ui.set_gesture)
        self.tracking_thread.hand_status_updated.connect(self.ui.set_hand_status)
        
        # Connect mode selector
        self.ui.mode_selector.currentTextChanged.connect(
            lambda mode: self.controller.set_mode(mode.lower())
        )
        self.ui.mode_selector.currentTextChanged.connect(
            lambda mode: self.ui.set_mode_display(mode)
        )
        
        # Connect re-calibration
        self.ui.recalibrate_requested.connect(self.recalibrate)
        
        # Start system
        self.start_system()
    
    def handle_gesture(self, x, y, distance):
        """Process gesture data and control cursor"""
        gesture_name = self.controller.process_gesture(
            x, y, distance, 
            self.tracking_thread.last_thumb_pos, 
            self.tracking_thread.last_index_pos,
            self.tracking_thread.last_landmarks
        )
        self.ui.set_gesture(gesture_name)
    
    def recalibrate(self):
        """Re-calibrate current user"""
        print(f"🔄 Re-calibrating user: {self.current_user}")
        
        # Pause tracking
        self.tracking_thread.pause()
        
        # Run calibration
        calibration = CalibrationScreen(user_name=self.current_user)
        calibration.show()
        calibration.exec_()
        
        # Get new calibration data
        self.calibration_data = calibration.get_calibration_data()
        self.controller.set_calibration(self.calibration_data)
        
        # Resume tracking
        self.tracking_thread.resume()
        print("✓ Re-calibration complete")
    
    def start_system(self):
        """Start the main system"""
        print("🚀 Starting AirOS...")
        print(f"👤 User: {self.current_user}")
        print("📷 Opening camera for hand tracking...")
        print("🖥️  Desktop UI ready")
        print("\nInstructions:")
        print("  - Point with index finger to move cursor")
        print("  - Pinch (thumb + index) to click")
        print("  - Swipe left/right to navigate")
        print("  - Press C to re-calibrate")
        print("  - Press Q in camera window to quit")
        print("  - Press ESC in desktop to quit\n")
        
        # Start hand tracking in background
        self.tracking_thread.start()
        
        # Show desktop UI
        self.ui.show()
    
    def run(self):
        """Run application"""
        exit_code = self.app.exec_()
        
        # Cleanup
        if hasattr(self, 'tracking_thread'):
            self.tracking_thread.stop()
            self.tracking_thread.wait()
        
        return exit_code

if __name__ == "__main__":
    airos = AirOS()
    sys.exit(airos.run())
