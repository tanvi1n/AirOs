# Testing Guide for AirOS

## ✅ What's Been Verified:
- Logic test passed: coordinate scaling and click detection work correctly
- Files created: gesture_control.py, desktop_ui.py, requirements.txt
- Dependencies installed in virtual environment

## 🧪 How to Test on Windows (Your Machine):

### Option 1: Test on Windows directly (RECOMMENDED)

Since you're on Windows (WSL), you need to test the GUI parts on Windows itself:

1. **Open Windows PowerShell or Command Prompt**
   - Navigate to: `C:\Users\Risha\Documents\projects\AirOs`

2. **Create Windows virtual environment:**
   ```powershell
   python -m venv venv_win
   venv_win\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Test gesture control (will move your cursor):**
   ```powershell
   python gesture_control.py
   ```
   - Your cursor should move to center, then top-left (and click), then bottom-right
   - Watch your cursor move!

4. **Test UI (will show fullscreen window):**
   ```powershell
   python desktop_ui.py
   ```
   - You'll see a fullscreen black window with 2 buttons
   - Click the buttons with your mouse to test
   - Press ESC to exit

### Option 2: Test logic only (works in WSL)

From WSL terminal:
```bash
cd /mnt/c/Users/Risha/Documents/projects/AirOs
source venv/bin/activate
python test_logic.py
```
This validates your coordinate scaling and click detection logic.

## 📋 What Each File Does:

**gesture_control.py:**
- Takes x, y (0-1 range) and distance from hand tracking
- Scales coordinates to screen size
- Moves cursor with pyautogui.moveTo()
- Clicks when distance < 30 (pinch detected)

**desktop_ui.py:**
- Fullscreen PyQt window (fake desktop)
- 2 clickable buttons
- Status label
- ESC to exit

**test_logic.py:**
- Tests coordinate scaling without GUI
- Tests click detection logic
- Safe to run in WSL

## 🔄 Next Steps for Tomorrow:

1. **Your friend creates:** `hand_tracking.py`
   - Webcam + MediaPipe
   - Outputs: x, y, distance

2. **Together you create:** `main.py`
   - Combines hand tracking + gesture control + UI
   - This is your demo file

## 🎯 Demo Flow Tomorrow:

```
Run main.py → Camera opens → Show hand → Cursor moves → Pinch → Button clicks
```

## ⚠️ Important Notes:

- **pyautogui and PyQt5 need a display** - test on Windows, not WSL
- The logic is correct (verified by test_logic.py)
- Your part is DONE - just needs integration with friend's hand tracking
- Keep threshold at 30 for now, adjust during integration if needed
