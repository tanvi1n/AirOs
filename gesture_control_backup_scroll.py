import pyautogui
import time
import math

# Get screen dimensions
screen_width, screen_height = pyautogui.size()

# Default thresholds
PINCH_THRESHOLD = 30

class GestureController:
    def __init__(self):
        self.click_cooldown = 0
        self.swipe_cooldown = 0
        self.mode = 'desktop'
        
        # STRONGER cursor smoothing (0.2 = 80% old, 20% new)
        self.prev_x = screen_width // 2
        self.prev_y = screen_height // 2
        self.smoothing_factor = 0.2  # Increased from 0.3
        
        # LONGER stability check
        self.pinch_frames = 0
        self.STABILITY_THRESHOLD = 3  # Increased from 2
        
        # Thumb direction tracking with LONGER stability
        self.thumb_direction_frames = 0
        self.last_thumb_direction = None
        self.THUMB_STABILITY = 4  # Need 8 consecutive frames
        
        # Thresholds
        self.pinch_threshold = PINCH_THRESHOLD
        self.thumb_threshold = 50  # Increased from 50 pixels
        
        self.current_gesture = "MOVE"
        
    def set_mode(self, mode):
        """Change gesture mode"""
        self.mode = mode.lower()
        print(f"🔄 Gesture mode: {self.mode.upper()}")
    
    def set_calibration(self, calibration_data):
        """Apply calibration data"""
        self.pinch_threshold = calibration_data.get('pinch_threshold', PINCH_THRESHOLD)
        # Use calibrated thumb threshold if available
        thumb_cal = calibration_data.get('swipe_threshold', 80)
        if isinstance(thumb_cal, (int, float)) and thumb_cal > 0:
            self.thumb_threshold = int(thumb_cal)
        print(f"✓ Calibration: pinch={self.pinch_threshold}, thumb={self.thumb_threshold}")
    
    def smooth_cursor(self, new_x, new_y):
        """Apply STRONG exponential smoothing"""
        smooth_x = int(self.smoothing_factor * new_x + (1 - self.smoothing_factor) * self.prev_x)
        smooth_y = int(self.smoothing_factor * new_y + (1 - self.smoothing_factor) * self.prev_y)
        self.prev_x, self.prev_y = smooth_x, smooth_y
        return smooth_x, smooth_y
    
    def detect_thumb_direction(self, thumb_pos, index_pos):
        """Detect thumb pointing left or right with STRONG stability"""
        if not thumb_pos or not index_pos:
            return None
        
        # Calculate horizontal distance
        thumb_x = thumb_pos[0]
        index_x = index_pos[0]
        horizontal_diff = thumb_x - index_x
        
        # Check cooldown
        current_time = time.time()
        if current_time < self.swipe_cooldown:
            return None
        
        # Determine direction with LARGER threshold
        if horizontal_diff < -self.thumb_threshold:
            direction = "LEFT"
        elif horizontal_diff > self.thumb_threshold:
            direction = "RIGHT"
        else:
            # Neutral position - reset
            self.thumb_direction_frames = 0
            self.last_thumb_direction = None
            return None
        
        # STRONG stability check: same direction for many frames
        if direction == self.last_thumb_direction:
            self.thumb_direction_frames += 1
        else:
            self.thumb_direction_frames = 1
            self.last_thumb_direction = direction
        
        # Only trigger after MANY stable frames
        if self.thumb_direction_frames >= self.THUMB_STABILITY:
            self.swipe_cooldown = current_time + 1.0  # Longer cooldown
            self.thumb_direction_frames = 0
            self.last_thumb_direction = None
            return direction
        
        return None
        
    def process_gesture(self, x, y, distance, thumb_pos=None, index_pos=None):
        """Process gestures with strong stability"""
        # Scale and smooth cursor
        mapped_x = int(x * screen_width)
        mapped_y = int(y * screen_height)
        smooth_x, smooth_y = self.smooth_cursor(mapped_x, mapped_y)
        pyautogui.moveTo(smooth_x, smooth_y, _pause=False)
        
        # Detect thumb direction
        swipe_direction = self.detect_thumb_direction(thumb_pos, index_pos)
        if swipe_direction:
            self.execute_swipe(swipe_direction)
            self.current_gesture = f"THUMB {swipe_direction}"
            return self.current_gesture
        
        # Pinch detection with STRONG stability
        current_time = time.time()
        if distance < self.pinch_threshold:
            self.pinch_frames += 1
            self.current_gesture = f"PINCHING... ({self.pinch_frames}/{self.STABILITY_THRESHOLD})"
        else:
            self.pinch_frames = 0
            self.current_gesture = "MOVE"
        
        # Only click after MANY stable frames
        if (self.pinch_frames >= self.STABILITY_THRESHOLD and 
            current_time > self.click_cooldown):
            self.execute_click()
            self.click_cooldown = current_time + 0.7  # Longer cooldown
            self.pinch_frames = 0
            self.current_gesture = "CLICK"
        
        return self.current_gesture
    
    def execute_click(self):
        """Context-aware click"""
        if self.mode == 'presentation':
            pyautogui.click(_pause=False)  # Allow clicking in presentation
            print("✓ NEXT SLIDE (Click)")
        elif self.mode == 'browser':
            pyautogui.click(_pause=False)
            print("✓ CLICK (Browser)")
        else:
            pyautogui.click(_pause=False)
            print("✓ CLICK")
    
    def execute_swipe(self, direction):
        """Context-aware swipe"""
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
