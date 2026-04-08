# AirOS - Complete Demo Guide

## ✅ What's Ready:

1. **hand_tracking.py** (Person 1) - Webcam + MediaPipe hand detection
2. **gesture_control.py** (Person 2) - Cursor movement + click detection  
3. **desktop_ui.py** (Person 2) - Desktop interface with apps
4. **main.py** (Integration) - Brings everything together

## 🚀 Running the Demo:

### On Windows PowerShell:

```powershell
cd C:\Users\Risha\Documents\projects\AirOs
venv_win\Scripts\activate
python main.py
```

## 🎯 What Happens:

1. **Camera window opens** - shows your hand with tracking
2. **Desktop UI appears** - fullscreen with app icons
3. **Move your hand** - cursor follows your index finger
4. **Pinch gesture** (thumb + index close together) - clicks

## 🎮 How to Use:

### Moving Cursor:
- Extend index finger (other fingers folded)
- Move hand left/right/up/down
- Cursor follows your finger tip

### Clicking:
- Bring thumb and index finger close together (pinch)
- When distance < 30 pixels → click happens
- Try clicking the desktop app icons!

### Exiting:
- Press **Q** in camera window, OR
- Press **ESC** in desktop window

## 🐛 Troubleshooting:

**Camera not opening?**
- Check if another app is using webcam
- Try unplugging/replugging webcam

**Cursor too fast/slow?**
- Adjust in gesture_control.py: change `duration=0.1` in moveTo()

**Clicks not working?**
- Adjust PINCH_THRESHOLD in gesture_control.py (currently 30)
- Lower number = easier to click
- Higher number = harder to click

**Hand not detected?**
- Ensure good lighting
- Keep hand in camera view
- Try adjusting min_detection_confidence in hand_tracking.py

## 📊 Demo Checklist:

✅ Camera opens and shows hand tracking
✅ Desktop UI displays with app icons
✅ Moving hand moves cursor
✅ Pinch gesture clicks buttons
✅ App windows open when clicked
✅ System is responsive

## 🎬 Demo Script:

"This is AirOS - a gesture-based desktop control system.

1. [Show camera feed] - Our system detects hand landmarks using MediaPipe
2. [Move hand] - Index finger position controls the cursor
3. [Pinch] - Pinch gesture triggers clicks
4. [Click app] - We can interact with desktop applications
5. [Open multiple apps] - Multiple windows can be managed

The system uses computer vision for hand tracking, coordinate mapping for cursor control, and PyQt for the desktop interface."

## 🔧 System Architecture:

```
Camera → MediaPipe → Hand Landmarks → Gesture Control → PyAutoGUI → Desktop UI
         (Person 1)                    (Person 2)                    (Person 2)
```

Good luck with your demo! 🎉
