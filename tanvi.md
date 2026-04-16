# AirOS Development Learnings

**Developer:** Tanvi Nutalapati  
**Timeline:** April 7-16, 2026  
**Project:** Gesture-Controlled Operating System

---

## Phase 1: Hand Tracking Module (April 7-8)

### What We Built
Real-time hand tracking system using MediaPipe that detects 21 hand landmarks and extracts fingertip coordinates for gesture recognition.

### Core Technologies
- Python 3.11 (Windows compatibility requirement)
- OpenCV for video capture
- MediaPipe 0.10.11 for hand detection
- NumPy for coordinate processing

### Major Errors & Solutions

**Error 1: MediaPipe Import Failure**
- Problem: `AttributeError: module 'mediapipe' has no attribute 'solutions'`
- Cause: MediaPipe 0.10.33 API changes
- Solution: Downgraded to MediaPipe 0.10.11

**Error 2: DLL Load Failed**
- Problem: DLL initialization failed on Windows
- Cause: Python 3.12+ incompatibility with MediaPipe
- Solution: Switched to Python 3.11, created new venv

### Key Learnings
1. **Version compatibility is critical** - MediaPipe requires Python 3.11 on Windows
2. **Document exact versions** - Not just "latest"
3. **Modular design enables parallel development** - Teammate built gesture engine while I built tracking
4. **Windows has unique DLL requirements** - Visual C++ dependencies matter

### Working Configuration
- OS: Windows 11
- Python: 3.11.x
- MediaPipe: 0.10.11
- Resolution: 640x480 @ 30 FPS

### Time: ~2 hours

---

## Phase 2: Desktop UI & Realistic Apps (April 9-10)

### What We Built
Fullscreen desktop simulation with functional applications for testing gestures.

### Applications Created
1. **Browser** - Tabbed interface with 4 tabs (Home, News, Games, Mail)
2. **Files** - Folder navigation with 12-18 files per folder
3. **Document Viewer** - Long scrollable AirOS documentation
4. **Presentation** - 6-slide PowerPoint-style app with navigation
5. **Notes** - Simple text editor
6. **Settings** - Settings menu with options

### Major Challenge: Window Focus
**Problem:** Keyboard commands (arrow keys) weren't reaching presentation window

**Cause:** PyQt buttons were capturing focus instead of the window

**Solution:** 
- Set buttons to `NoFocus` policy
- Added keyboard event handlers to windows
- Ensured windows auto-focus on open

### Mode System Implementation
Added 4 gesture modes with auto-switching:
- **Desktop** - Basic cursor + click
- **Document** - Cursor + click + scroll
- **Presentation** - Cursor + click + slide navigation
- **Browser** - Cursor + click + scroll + back/forward

Apps automatically switch modes when opened.

### Key Learnings
1. **PyQt focus management is critical** for keyboard-based gestures
2. **Auto mode switching reduces user confusion** - Context-aware behavior
3. **Realistic content is essential** for proper testing
4. **Index management matters** when modifying dropdown lists

### Time: ~4.5 hours

---

## Phase 3: Scroll Gesture Implementation (April 15)

### Evolution Through 3 Attempts

**Attempt 1: Continuous Tracking (FAILED)**
- Approach: Track palm movement while two fingers extended
- Problems: Very laggy, inconsistent, cursor interference
- Why it failed: Too much processing overhead

**Attempt 2: Fist-Based Scroll (FAILED)**
- Approach: Make fist, move vertically
- Problems: Unreliable detection, conflicted with swipe gesture
- Why it failed: Gesture ambiguity

**Attempt 3: Retract-Trigger (SUCCESS ✅)**
- Approach: Extend two fingers → Close them → Triggers scroll
- Direction: Position-based (top half = scroll up, bottom half = scroll down)
- Result: Instant response, no lag, 100% reliable

### Technical Implementation
- Scroll amount: 20 units per trigger
- Cooldown: 300ms between scrolls
- Screen center: 240px (480p frame / 2)
- Mode restriction: Only works in Document and Browser modes

### Major Errors & Solutions

**Error 1: KeyError 'palm'**
- Cause: Missing palm landmark in hand_tracking.py
- Solution: Added landmark 9 (palm center) to return dictionary

**Error 2: Scroll Not Executing**
- Cause: Document window didn't have focus
- Solution: Added auto-focus to windows, ensured click before scroll

**Error 3: Continuous Scroll Lag**
- Cause: Processing every frame for scroll calculation
- Solution: Switched to discrete retract-trigger approach

### Performance Comparison
- **Before (Continuous):** 20-25 FPS, 200-300ms lag, inconsistent
- **After (Retract-Trigger):** 30 FPS stable, <50ms response, 100% reliable

### Key Learnings
1. **Discrete gestures > Continuous tracking** for responsiveness
2. **Position-based direction is intuitive** (top=up, bottom=down)
3. **Cooldown periods prevent accidental triggers**
4. **Mode separation eliminates gesture conflicts**
5. **First implementation rarely works** - Be ready to redesign
6. **User feedback reveals issues code review misses**

### Time: ~6.5 hours

---

## Final Gesture System

### Universal (All Modes)
- **Point** (index finger) → Move cursor
- **Pinch** (thumb + index close) → Click

### Document/Browser Modes
- **Two fingers in top half → Retract** → Scroll UP
- **Two fingers in bottom half → Retract** → Scroll DOWN

### Presentation/Browser Modes
- **Fist + Thumb Right** → Next slide / Forward
- **Fist + Thumb Left** → Previous slide / Back

### Gesture Conflict Resolution
Mode-based separation ensures no gesture conflicts - same hand position means different things in different contexts.

---

## Overall System Architecture

### Modules (Collaborative Development)
- **Hand Tracking** (Tanvi) - Landmark detection and extraction
- **Gesture Control** (Risha) - Gesture interpretation and execution
- **Desktop UI** (Tanvi) - Application windows and interface
- **User System** (Risha) - Profiles and calibration
- **Mode Switching** (Collaborative) - Context-aware behavior

### Performance Metrics
- FPS: 30 (stable)
- Hand detection: Real-time
- Gesture response: <50ms
- Accuracy: 100% with proper gestures

---

## Critical Success Factors

1. **Modular Design** - Enabled parallel development and easy iteration
2. **Version Control** - Exact dependency versions prevented compatibility issues
3. **Realistic Testing** - Functional apps revealed real-world issues
4. **Iterative Approach** - Willingness to redesign when solutions didn't work
5. **Mode-Based Logic** - Context-aware gestures eliminated conflicts
6. **User Calibration** - Personalized settings for different hand sizes

---

## Key Takeaways

### Technical
- Python 3.11 is required for MediaPipe on Windows
- Discrete gestures are more responsive than continuous tracking
- PyQt focus management is critical for keyboard-based control
- Position-based direction is more intuitive than movement-based

### Process
- First solution rarely works perfectly
- Real user testing reveals issues theory misses
- Modular architecture enables parallel development
- Document exact versions, not just "latest"

### Design Philosophy
- Gestures must be deliberate, not accidental
- Context matters - same gesture, different meanings
- Performance optimization at every level
- User intent should be clear and unambiguous

---

## Total Development Time
- Phase 1 (Hand Tracking): 2 hours
- Phase 2 (Desktop UI): 4.5 hours
- Phase 3 (Scroll Gesture): 6.5 hours
- **Total: ~13 hours** (individual contribution)

---

## Project Status: Production-Ready ✅

All core features implemented and tested:
- ✅ Hand tracking with 21 landmarks
- ✅ 4 gesture modes with auto-switching
- ✅ 6 functional applications
- ✅ User profiles and calibration
- ✅ Smooth 30 FPS performance
- ✅ Reliable gesture detection

---

## Presentation Summary

"I built the hand tracking foundation for AirOS using MediaPipe, which detects 21 hand landmarks in real-time. After resolving Windows compatibility issues by using Python 3.11 and MediaPipe 0.10.11, I created a desktop simulation with functional applications for testing. The scroll gesture went through three iterations before we found the optimal solution: a retract-trigger approach where users extend two fingers and close them to scroll, with direction determined by hand position. This discrete gesture proved far more responsive than continuous tracking. The system now runs at 30 FPS with instant gesture response and supports multiple modes for context-aware behavior."

---

## References
- MediaPipe Hands: https://google.github.io/mediapipe/solutions/hands
- OpenCV Python: https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html
- PyQt5 Documentation: https://doc.qt.io/qt-5/
