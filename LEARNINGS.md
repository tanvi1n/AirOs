# AirOS Development Learnings

## Project: Hand Tracking Module

**Date:** April 7-8, 2026  
**Developer:** Tanvi Nutalapati  
**Module:** Hand Tracking (Foundation Layer)

---

## What We Built

A real-time hand tracking system that:
- Captures webcam input using OpenCV
- Detects hand landmarks using MediaPipe
- Extracts fingertip coordinates (index and thumb)
- Provides structured data output for gesture recognition
- Works as both standalone module and importable class

---

## Technical Implementation

### Core Technologies
- **Python 3.11** (specific version required)
- **OpenCV** for video capture and display
- **MediaPipe 0.10.11** for hand landmark detection
- **NumPy** for coordinate processing

### Architecture Decision
Chose **modular class-based design** because:
- Enables parallel development with gesture engine team
- Allows standalone testing without dependencies
- Clean integration through simple import
- Easy to extend with additional landmarks later

### Key Code Structure
```python
class HandTracker:
    - __init__(): Initialize MediaPipe
    - extract_landmarks(frame): Core detection logic
    - run(): Standalone test mode
```

---

## Errors Faced & Solutions

### Error 1: MediaPipe Import Failure
**Error:**
```
AttributeError: module 'mediapipe' has no attribute 'solutions'
```

**Cause:** MediaPipe 0.10.33 had API changes that broke `mp.solutions` access

**Attempted Solutions:**
1. ❌ Tried updating import structure - didn't work
2. ❌ Attempted to use newer MediaPipe API - too complex
3. ❌ Tried version 0.10.9 - not available for Windows

**Final Solution:** ✅ Downgraded to MediaPipe 0.10.11 (stable version with `mp.solutions` support)

---

### Error 2: DLL Load Failed
**Error:**
```
ImportError: DLL load failed while importing _framework_bindings: 
A dynamic link library (DLL) initialization routine failed
```

**Cause:** MediaPipe requires specific Visual C++ runtime libraries on Windows + Python version compatibility issues

**Attempted Solutions:**
1. ❌ Installed Visual C++ Redistributable - didn't resolve
2. ❌ Tried different MediaPipe versions (0.10.14, 0.10.21) - same error
3. ❌ Attempted opencv-contrib-python - not the root cause

**Final Solution:** ✅ Switched from Python 3.12+ to Python 3.11
- Created new virtual environment with Python 3.11
- Reinstalled all dependencies
- Used MediaPipe 0.10.11

---

## Key Learnings

### 1. Version Compatibility Matters
- MediaPipe has strict Python version requirements on Windows
- Python 3.11 is the sweet spot for MediaPipe on Windows
- Always check library compatibility before starting

### 2. Windows-Specific Issues
- DLL errors are common with computer vision libraries on Windows
- Visual C++ dependencies can cause silent failures
- WSL vs native Windows can have different behaviors

### 3. Dependency Management
- Virtual environments are essential for version control
- Document exact working versions (not just "latest")
- Test on target platform early

### 4. Modular Design Benefits
- Standalone testing caught issues before integration
- Clear interfaces make parallel development possible
- Easy to debug when components are isolated

### 5. MediaPipe API Evolution
- Older versions use `mp.solutions.hands`
- Newer versions (0.10.30+) use task-based API
- Legacy API still works in 0.10.11-0.10.21 range

---

## Working Configuration

### Environment
- **OS:** Windows 11
- **Python:** 3.11.x
- **Virtual Environment:** venv

### Dependencies (Exact Versions)
```
opencv-python
mediapipe==0.10.11
numpy
```

### Installation Steps That Worked
```bash
# Create venv with Python 3.11
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install opencv-python mediapipe==0.10.11 numpy
```

---

## Testing & Validation

### What Works
✅ Real-time hand detection at 30+ FPS  
✅ Accurate landmark visualization  
✅ Precise fingertip coordinate extraction  
✅ Smooth tracking with minimal jitter  
✅ Handles hand entering/leaving frame gracefully  

### Test Commands
```bash
# Standalone test
python hand_tracking.py

# Exit with 'q' key
```

---

## Integration Notes for Team

### For Gesture Engine Developer
Import and use like this:
```python
from hand_tracking import HandTracker

tracker = HandTracker()
landmarks = tracker.extract_landmarks(frame)

if landmarks:
    index_pos = landmarks["index_tip"]
    thumb_pos = landmarks["thumb_tip"]
    # Your gesture detection logic here
```

### Data Format
```python
# When hand detected:
{
    "index_tip": (x, y),  # pixel coordinates
    "thumb_tip": (x, y)
}

# When no hand detected:
None
```

---

## Future Improvements

### Potential Enhancements
- Add more landmark points (middle finger, wrist, etc.)
- Multi-hand support (currently single hand)
- Confidence score output
- FPS counter for performance monitoring
- Configurable detection thresholds

### Known Limitations
- Single hand detection only
- Requires good lighting
- Performance depends on webcam quality
- No gesture interpretation (by design - that's next module)

---

## Time Investment

- Initial setup & coding: 30 minutes
- Debugging MediaPipe issues: 45 minutes
- Python version troubleshooting: 30 minutes
- Testing & validation: 15 minutes
- **Total:** ~2 hours

---

## Presentation Talking Points

"I implemented the hand tracking module using MediaPipe, which detects 21 hand landmarks in real-time. The system extracts precise fingertip coordinates and provides them in a structured format for the gesture recognition engine. We faced compatibility challenges with MediaPipe on Windows, which we resolved by using Python 3.11 and MediaPipe version 0.10.11. The module works both standalone for testing and as an importable component for system integration."

---

## References & Resources

- MediaPipe Hands Documentation: https://google.github.io/mediapipe/solutions/hands
- OpenCV Python Tutorials: https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html
- MediaPipe Version Compatibility: https://pypi.org/project/mediapipe/#history

---

## Conclusion

Successfully built the foundation layer of AirOS. The hand tracking module is production-ready and provides reliable coordinate data for gesture recognition. Key takeaway: version compatibility and platform-specific issues require careful attention in computer vision projects.
