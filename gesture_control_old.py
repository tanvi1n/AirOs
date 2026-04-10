import pyautogui
import time
import math

# Get screen dimensions
screen_width, screen_height = pyautogui.size()

# Default thresholds (can be overridden by calibration)
PINCH_THRESHOLD = 30
SWIPE_THRESHOLD = 0.15  # Not used for thumb direction

class GestureController:
    def __init__(self):
        self.click_cooldown = 0
        self.swipe_cooldown = 0
        self.mode = 'desktop'
        
        # Cursor smoothing
        self.prev_x = screen_width // 2
        self.prev_y = screen_height // 2
        self.smoothing_factor = 0.3
        
        # Stability check
        self.pinch_frames = 0
        self.STABILITY_THRESHOLD = 2
        
        # Thumb direction tracking
        self.thumb_direction_frames = 0
        self.last_thumb_direction = None
        
        # Thresholds
        self.pinch_threshold = PINCH_THRESHOLD
        self.swipe_threshold = SWIPE_THRESHOLD
        
        self.current_gesture = "MOVE"
        
    def set_mode(self, mode):
        """Change gesture mode (desktop/presentation/browser)"""
        self.mode = mode.lower()
        print(f"🔄 Gesture mode: {self.mode.upper()}")
    
    def set_calibration(self, calibration_data):
        """Apply calibration data"""
        self.pinch_threshold = calibration_data.get('pinch_threshold', PINCH_THRESHOLD)
        self.swipe_threshold = calibration_data.get('swipe_threshold', SWIPE_THRESHOLD)
        print(f"✓ Calibration applied: pinch={self.pinch_threshold}")
    
    def smooth_cursor(self, new_x, new_y):
        """Apply exponential smoothing to cursor movement"""
        smooth_x = int(self.smoothing_factor * new_x + (1 - self.smoothing_factor) * self.prev_x)
        smooth_y = int(self.smoothing_factor * new_y + (1 - self.smoothing_factor) * self.prev_y)
        self.prev_x, self.prev_y = smooth_x, smooth_y
        return smooth_x, smooth_y
    
    def detect_thumb_direction(self, thumb_pos, index_pos):
        """Detect thumb pointing left or right relative to index finger"""
        # Calculate horizontal distance
        thumb_x = thumb_pos[0]
        index_x = index_pos[0]
        
        horizontal_diff = thumb_x - index_x
        
        # Threshold: thumb must be significantly left or right of index
        threshold = 50  # pixels
        
        current_time = time.time()
        if current_time < self.swipe_cooldown:
            return None
        
        if horizontal_diff < -threshold:
            # Thumb is LEFT of index finger
            direction = "LEFT"
        elif horizontal_diff > threshold:
            # Thumb is RIGHT of index finger
            direction = "RIGHT"
        else:
            # Thumb is neutral (near index)
            self.thumb_direction_frames = 0
            self.last_thumb_direction = None
            return None
        
        # Stability check: same direction for 3 frames
        if direction == self.last_thumb_direction:
            self.thumb_direction_frames += 1
        else:
            self.thumb_direction_frames = 1
            self.last_thumb_direction = direction
        
        if self.thumb_direction_frames >= 3:
            self.swipe_cooldown = current_time + 0.8
            self.thumb_direction_frames = 0
            return direction
        
        return None
        
    def process_gesture(self, x, y, distance, thumb_pos=None, index_pos=None):
        """Convert hand coordinates to cursor movement and clicks"""
        # Scale normalized coordinates (0-1) to screen size
        mapped_x = int(x * screen_width)
        mapped_y = int(y * screen_height)
        
        # Apply cursor smoothing
        smooth_x, smooth_y = self.smooth_cursor(mapped_x, mapped_y)
        pyautogui.moveTo(smooth_x, smooth_y, _pause=False)
        
        # Detect thumb direction for swipe
        if thumb_pos and index_pos:
            swipe_direction = self.detect_thumb_direction(thumb_pos, index_pos)
            if swipe_direction:
                self.execute_swipe(swipe_direction)
                self.current_gesture = f"THUMB {swipe_direction}"
                return self.current_gesture
        
        # Stability check for pinch
        current_time = time.time()
        if distance < self.pinch_threshold:
            self.pinch_frames += 1
            self.current_gesture = "PINCHING..."
        else:
            self.pinch_frames = 0
            self.current_gesture = "MOVE"
        
        # Execute click only if stable and cooldown passed
        if (self.pinch_frames >= self.STABILITY_THRESHOLD and 
            current_time > self.click_cooldown):
            self.execute_click()
            self.click_cooldown = current_time + 0.5
            self.pinch_frames = 0
            self.current_gesture = "CLICK"
        
        return self.current_gesture
    
    def execute_click(self):
        """Context-aware click action"""
        if self.mode == 'presentation':
            pyautogui.press('right')
            print("✓ NEXT SLIDE")
        elif self.mode == 'browser':
            pyautogui.click(_pause=False)
            print("✓ CLICK (Browser)")
        else:
            pyautogui.click(_pause=False)
            print("✓ CLICK")
    
    def execute_swipe(self, direction):
        """Context-aware swipe action"""
        if self.mode == 'presentation':
            if direction == "RIGHT":
                pyautogui.press('right')
                print("✓ NEXT SLIDE (Thumb Right)")
            elif direction == "LEFT":
                pyautogui.press('left')
                print("✓ PREVIOUS SLIDE (Thumb Left)")
        elif self.mode == 'browser':
            if direction == "LEFT":
                pyautogui.hotkey('alt', 'left')
                print("✓ BACK (Browser)")
            elif direction == "RIGHT":
                pyautogui.hotkey('alt', 'right')
                print("✓ FORWARD (Browser)")
        else:
            print(f"✓ THUMB {direction}")
