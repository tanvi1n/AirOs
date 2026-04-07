# ✨ AirOS – A Self-Calibrating Gesture-Based Desktop Interaction System

## 📌 Overview

AirOS is a gesture-controlled desktop interaction system designed to replace traditional input devices like the mouse and keyboard with natural hand movements. Using computer vision and real-time hand tracking, AirOS enables touchless interaction with a computer system.

The project focuses on improving accessibility, enabling hands-free control, and creating an intuitive interaction experience using gestures.

---

## 🚨 Problem Statement

Traditional computer interaction relies heavily on physical devices such as a mouse and keyboard. This creates limitations:

* ❌ No support for touchless interaction
* ❌ Difficult for users with limited hand mobility
* ❌ Not suitable for environments like classrooms or presentations
* ❌ Lack of practical gesture-based desktop systems

---

## 🎯 Objective

To design and implement a **self-calibrating, gesture-based desktop system** that:

* Detects hand movements in real-time
* Interprets gestures accurately
* Maps gestures to system-level actions
* Simulates a lightweight desktop interface

---

## 🚀 Key Features

* 🖐️ **Real-Time Hand Tracking** using webcam input
* ⚙️ **Self-Calibrating System** that adapts to user movement
* 🎯 **Gesture Detection Engine** for interpreting hand gestures
* 🖱️ **Virtual Cursor Control** using fingertip tracking
* 🔄 **Adaptive Sensitivity Engine** to reduce errors
* 🧭 **Gesture-Based Navigation System**
* ✍️ **AirWrite Mode** for finger-based writing
* 🎛️ **Mini Desktop Simulation** with app modules
* 🧩 **Modular Architecture** for scalability

---

## 🏗️ System Architecture

```
Camera Input
     ↓
Hand Landmark Detection (MediaPipe)
     ↓
Gesture Detection Engine
     ↓
Adaptive Motion Engine
     ↓
Virtual Cursor Controller
     ↓
Mini Desktop Simulation Layer
     ↓
Application Modules
```

---

## 🧠 Core Modules

### 1. Hand Tracking Module

* Uses MediaPipe to detect hand landmarks
* Extracts key points like fingertips and joints

### 2. Gesture Detection Engine

* Interprets gestures such as:

  * Pinch → Click
  * Swipe → App switching
  * Open Palm → Home
  * Fist → Drag

### 3. Adaptive Engine

* Calibrates sensitivity based on user movement
* Reduces jitter and improves accuracy

### 4. Virtual Cursor Controller

* Maps finger position to screen coordinates
* Enables smooth cursor movement

### 5. Mini Desktop Simulation

* Lightweight UI environment
* Supports gesture-based navigation

### 6. Application Modules

* Notes
* Settings
* Info panel
* AirWrite

---

## 🛠️ Tech Stack

| Category        | Technology Used   |
| --------------- | ----------------- |
| Programming     | Python 3.11       |
| Computer Vision | MediaPipe, OpenCV |
| UI Framework    | PyQt6             |
| Processing      | NumPy             |

All tools used are open-source and locally executable.

**Note:** Python 3.11 is required for MediaPipe compatibility on Windows.

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repo-link>
cd airOS
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install opencv-python mediapipe numpy pyautogui pyqt6
```

---

## ▶️ Running the Project

```bash
python main.py
```

Ensure your webcam is connected.

---

## 🧪 Current Progress (MVP)

The current implementation includes:

* ✅ Real-time hand detection
* ✅ Landmark visualization
* ✅ Basic gesture recognition (e.g., pinch)
* ✅ Cursor control using finger tracking

This forms the foundation for the full AirOS system.

---

## 🔮 Future Scope

* Full desktop UI implementation
* Multi-hand gesture support
* Custom gesture training
* Integration with OS-level controls
* Voice + gesture hybrid system
* AI-based gesture prediction

---

## 📚 References

* Gesture Controlled Virtual Mouse using AI
* Hand Tracking Based Virtual Mouse System
* Augmented Virtual Mouse System
* Other research papers (see project documentation)

---

## 👩‍💻 Contributors

* Tanvi Nutalapati
* Balagam Risha Raj

---

## 🙌 Acknowledgment

We thank our mentor for guidance and support throughout the development of this project.

---

## 💡 Conclusion

AirOS demonstrates how computer vision and gesture recognition can redefine human-computer interaction by making it more natural, accessible, and futuristic.

---
