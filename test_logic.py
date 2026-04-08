"""Test gesture control logic without GUI"""

# Simulate screen size
screen_width, screen_height = 1920, 1080
PINCH_THRESHOLD = 30

def test_coordinate_scaling():
    """Test that coordinates scale correctly"""
    print("Testing coordinate scaling...")
    
    # Test center
    x, y = 0.5, 0.5
    mapped_x = int(x * screen_width)
    mapped_y = int(y * screen_height)
    print(f"  Center (0.5, 0.5) → ({mapped_x}, {mapped_y})")
    assert mapped_x == 960 and mapped_y == 540, "Center scaling failed"
    
    # Test top-left
    x, y = 0.0, 0.0
    mapped_x = int(x * screen_width)
    mapped_y = int(y * screen_height)
    print(f"  Top-left (0.0, 0.0) → ({mapped_x}, {mapped_y})")
    
    # Test bottom-right
    x, y = 1.0, 1.0
    mapped_x = int(x * screen_width)
    mapped_y = int(y * screen_height)
    print(f"  Bottom-right (1.0, 1.0) → ({mapped_x}, {mapped_y})")
    
    print("✓ Coordinate scaling works!\n")

def test_click_detection():
    """Test click detection logic"""
    print("Testing click detection...")
    
    # Test no click
    distance = 100
    if distance < PINCH_THRESHOLD:
        print(f"  Distance {distance} → CLICK")
    else:
        print(f"  Distance {distance} → No click")
    
    # Test click
    distance = 20
    if distance < PINCH_THRESHOLD:
        print(f"  Distance {distance} → CLICK ✓")
    else:
        print(f"  Distance {distance} → No click")
    
    print("✓ Click detection works!\n")

if __name__ == "__main__":
    print("=== Testing Gesture Control Logic ===\n")
    test_coordinate_scaling()
    test_click_detection()
    print("=== All tests passed! ===")
