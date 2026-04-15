import pyautogui
import time
import math

screen_width, screen_height = pyautogui.size()
PINCH_THRESHOLD = 30

class GestureController:
    def __init__(self):
        self.click_cooldown = 0
        self.swipe_cooldown = 0
        self.mode = 'desktop'
        
        self.prev_x = screen_width // 2
        self.prev_y = screen_height // 2
        self.smoothing_factor = 0.2
        
        self.pinch_frames = 0
        self.STABILITY_THRESHOLD = 3
        
        self.thumb_direction_frames = 0
        self.last_thumb_direction = None
        self.THUMB_STABILITY = 4
        
        # Scroll tracking
        self.prev_fingers_extended = False  # Track finger state
        self.scroll_cooldown_time = 0  # Prevent rapid triggers
        self.scroll_amount_per_trigger = 100  # Increased from 5 to 20
        self.last_finger_y = None  # Track finger position for direction
        self.last_finger_y = None  # Track finger position for direction
        
        self.pinch_threshold = PINCH_THRESHOLD
        self.thumb_threshold = 50
        
        self.current_gesture = "MOVE"
        
    def set_mode(self, mode):
        self.mode = mode.lower()
        print(f"🔄 Gesture mode: {self.mode.upper()}")
    
    def set_calibration(self, calibration_data):
        self.pinch_threshold = calibration_data.get('pinch_threshold', PINCH_THRESHOLD)
        thumb_cal = calibration_data.get('swipe_threshold', 50)
        if isinstance(thumb_cal, (int, float)) and thumb_cal > 0:
            self.thumb_threshold = int(thumb_cal)
        print(f"✓ Calibration: pinch={self.pinch_threshold}, thumb={self.thumb_threshold}")
    
    def smooth_cursor(self, new_x, new_y):
        smooth_x = int(self.smoothing_factor * new_x + (1 - self.smoothing_factor) * self.prev_x)
        smooth_y = int(self.smoothing_factor * new_y + (1 - self.smoothing_factor) * self.prev_y)
        self.prev_x, self.prev_y = smooth_x, smooth_y
        return smooth_x, smooth_y
    
    def are_two_fingers_extended(self, landmarks):
        """Check if index and middle fingers are extended"""
        if not landmarks:
            return False
        
        index_extended = landmarks['index_tip'][1] < landmarks['index_pip'][1]
        middle_extended = landmarks['middle_tip'][1] < landmarks['middle_pip'][1]
        
        return index_extended and middle_extended
    
    def detect_scroll(self, landmarks):
        """Detect scroll: extend two fingers in top/bottom half, then retract"""
        # Only in document/browser modes
        if self.mode not in ['document', 'browser']:
            self.prev_fingers_extended = False
            self.last_finger_y = None
            return None
        
        if not landmarks:
            return None
        
        current_time = time.time()
        
        # Check if cooldown active
        if current_time < self.scroll_cooldown_time:
            return None
        
        fingers_extended = self.are_two_fingers_extended(landmarks)
        
        # Track finger position when extended
        if fingers_extended:
            # Use average of index and middle finger Y position
            current_y = (landmarks['index_tip'][1] + landmarks['middle_tip'][1]) // 2
            self.last_finger_y = current_y
        
        # Detect retract: was extended, now closed
        if self.prev_fingers_extended and not fingers_extended:
            if self.last_finger_y is not None:
                # Screen center (assuming 480p from hand tracking)
                screen_center_y = 240  # 480 / 2
                
                # Determine direction based on position
                if self.last_finger_y < screen_center_y:
                    # Top half → Scroll UP
                    direction = "UP"
                    scroll_amount = self.scroll_amount_per_trigger
                else:
                    # Bottom half → Scroll DOWN
                    direction = "DOWN"
                    scroll_amount = -self.scroll_amount_per_trigger
                
                self.scroll_cooldown_time = current_time + 0.3
                self.prev_fingers_extended = False
                self.last_finger_y = None
                print(f"📜 SCROLL {direction} (position-based)")
                return (direction, scroll_amount)
        
        # Update state
        self.prev_fingers_extended = fingers_extended
        return None
    
    def detect_thumb_direction(self, thumb_pos, index_pos):
        """Detect thumb pointing left or right"""
        if not thumb_pos or not index_pos:
            return None
        
        thumb_x = thumb_pos[0]
        index_x = index_pos[0]
        horizontal_diff = thumb_x - index_x
        
        current_time = time.time()
        if current_time < self.swipe_cooldown:
            return None
        
        if horizontal_diff < -self.thumb_threshold:
            direction = "LEFT"
        elif horizontal_diff > self.thumb_threshold:
            direction = "RIGHT"
        else:
            self.thumb_direction_frames = 0
            self.last_thumb_direction = None
            return None
        
        if direction == self.last_thumb_direction:
            self.thumb_direction_frames += 1
        else:
            self.thumb_direction_frames = 1
            self.last_thumb_direction = direction
        
        if self.thumb_direction_frames >= self.THUMB_STABILITY:
            self.swipe_cooldown = current_time + 1.0
            self.thumb_direction_frames = 0
            self.last_thumb_direction = None
            return direction
        
        return None
        
    def process_gesture(self, x, y, distance, thumb_pos=None, index_pos=None, landmarks=None):
        """Process gestures with scroll detection"""
        
        # Check for scroll gesture first (two fingers extended)
        scroll_result = self.detect_scroll(landmarks)
        if scroll_result:
            direction, amount = scroll_result
            pyautogui.scroll(amount)
            self.current_gesture = f"SCROLL {direction}"
            print(f"📜 SCROLL {direction}")
            return self.current_gesture
        
        # Normal cursor movement (only if not scrolling)
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
        
        # Pinch detection
        current_time = time.time()
        if distance < self.pinch_threshold:
            self.pinch_frames += 1
            self.current_gesture = f"PINCHING... ({self.pinch_frames}/{self.STABILITY_THRESHOLD})"
        else:
            self.pinch_frames = 0
            self.current_gesture = "MOVE"
        
        if (self.pinch_frames >= self.STABILITY_THRESHOLD and 
            current_time > self.click_cooldown):
            self.execute_click()
            self.click_cooldown = current_time + 0.7
            self.pinch_frames = 0
            self.current_gesture = "CLICK"
        
        return self.current_gesture
    
    def execute_click(self):
        if self.mode == 'presentation':
            pyautogui.click(_pause=False)
            print("✓ CLICK (Presentation)")
        elif self.mode == 'browser':
            pyautogui.click(_pause=False)
            print("✓ CLICK (Browser)")
        else:
            pyautogui.click(_pause=False)
            print("✓ CLICK")
    
    def execute_swipe(self, direction):
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
