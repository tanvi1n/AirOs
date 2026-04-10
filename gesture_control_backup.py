import pyautogui
import time

# Get screen dimensions
screen_width, screen_height = pyautogui.size()

# Pinch threshold for click detection
PINCH_THRESHOLD = 30

class GestureController:
    def __init__(self):
        self.click_cooldown = 0
        
    def process_gesture(self, x, y, distance):
        """Convert hand coordinates to cursor movement and clicks"""
        # Scale normalized coordinates (0-1) to screen size
        mapped_x = int(x * screen_width)
        mapped_y = int(y * screen_height)
        
        # Move cursor instantly (no duration for smoothness)
        pyautogui.moveTo(mapped_x, mapped_y, _pause=False)
        
        # Detect pinch click
        current_time = time.time()
        if distance < PINCH_THRESHOLD and current_time > self.click_cooldown:
            pyautogui.click(_pause=False)
            self.click_cooldown = current_time + 0.5  # Prevent double clicks
            print(f"✓ CLICK! (distance: {distance:.1f})")

# Test with dummy data
if __name__ == "__main__":
    controller = GestureController()
    
    print("Testing cursor control with dummy data...")
    print(f"Screen size: {screen_width}x{screen_height}\n")
    
    # Test 1: Move to center
    print("1. Moving to center...")
    controller.process_gesture(0.5, 0.5, 100)
    time.sleep(1)
    
    # Test 2: Move to top-left and click
    print("2. Moving to top-left and clicking...")
    controller.process_gesture(0.3, 0.3, 20)
    time.sleep(1)
    
    # Test 3: Move to bottom-right
    print("3. Moving to bottom-right...")
    controller.process_gesture(0.7, 0.7, 100)
    
    print("\n✓ Test complete!")
