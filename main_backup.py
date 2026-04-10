import sys
import cv2
import math
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal
from hand_tracking import HandTracker
from gesture_control import GestureController
from desktop_ui import DesktopUI

class HandTrackingThread(QThread):
    """Thread to run hand tracking without blocking UI"""
    gesture_detected = pyqtSignal(float, float, float)
    
    def __init__(self):
        super().__init__()
        self.tracker = HandTracker()
        self.running = True
        
    def run(self):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Lower resolution
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)  # Limit FPS
        
        while self.running and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                continue
            
            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            
            landmarks = self.tracker.extract_landmarks(frame)
            
            if landmarks:
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
                
                # Emit gesture data
                self.gesture_detected.emit(x, y, distance)
                
                # Minimal visual feedback (less drawing = faster)
                cv2.circle(frame, index_tip, 8, (0, 255, 0), -1)
                cv2.circle(frame, thumb_tip, 8, (255, 0, 0), -1)
            
            # Show frame at lower quality for speed
            cv2.imshow('AirOS - Hand Tracking (Press Q to quit)', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.running = False
                break
        
        cap.release()
        cv2.destroyAllWindows()
    
    def stop(self):
        self.running = False

class AirOS:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.ui = DesktopUI()
        self.controller = GestureController()
        self.tracking_thread = HandTrackingThread()
        
        # Connect hand tracking to gesture control
        self.tracking_thread.gesture_detected.connect(self.handle_gesture)
        
    def handle_gesture(self, x, y, distance):
        """Process gesture data and control cursor"""
        self.controller.process_gesture(x, y, distance)
    
    def run(self):
        """Start the system"""
        print("🚀 Starting AirOS...")
        print("📷 Opening camera for hand tracking...")
        print("🖥️  Desktop UI ready")
        print("\nInstructions:")
        print("  - Point with index finger to move cursor")
        print("  - Pinch (thumb + index) to click")
        print("  - Press Q in camera window to quit")
        print("  - Press ESC in desktop to quit\n")
        
        # Start hand tracking in background
        self.tracking_thread.start()
        
        # Show desktop UI
        self.ui.show()
        
        # Run application
        exit_code = self.app.exec_()
        
        # Cleanup
        self.tracking_thread.stop()
        self.tracking_thread.wait()
        
        return exit_code

if __name__ == "__main__":
    airos = AirOS()
    sys.exit(airos.run())
