from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QVBoxLayout, 
                             QHBoxLayout, QFrame, QScrollArea, QTextEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class DocumentViewer(QWidget):
    """Scrollable document viewer for testing scroll gestures"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: white;")
        self.resize(800, 700)
        
        from PyQt5.QtWidgets import QApplication
        screen = QApplication.desktop().screenGeometry()
        self.move((screen.width() - 800) // 2, (screen.height() - 700) // 2)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Title bar
        title_bar = self.create_title_bar("Document Viewer")
        layout.addWidget(title_bar)
        
        # Scrollable text area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")
        
        text_widget = QTextEdit()
        text_widget.setReadOnly(True)
        text_widget.setStyleSheet("font-size: 14px; padding: 40px; line-height: 1.6;")
        
        # Sample document content
        document_text = """
<h2>AirOS: Gesture-Controlled Operating System</h2>
<h3>Project Documentation</h3>

<p><b>Introduction</b></p>
<p>AirOS is an innovative gesture-controlled operating system that allows users to interact with their computer using hand movements captured through a webcam. This document provides an overview of the system architecture, features, and implementation details.</p>

<p><b>System Architecture</b></p>
<p>The system consists of three main components:</p>
<ul>
<li>Hand Tracking Module: Captures webcam input and detects hand landmarks using MediaPipe</li>
<li>Gesture Recognition Engine: Interprets hand movements and converts them into system commands</li>
<li>Desktop UI: Provides a simulated desktop environment for demonstration</li>
</ul>

<p><b>Key Features</b></p>
<p>1. Real-time Hand Detection: The system uses MediaPipe's hand tracking solution to detect 21 hand landmarks in real-time with high accuracy.</p>

<p>2. Cursor Control: Users can move the cursor by pointing with their index finger. The system maps hand coordinates to screen coordinates smoothly.</p>

<p>3. Click Interaction: A pinch gesture (bringing thumb and index finger together) triggers a click action, allowing users to interact with UI elements.</p>

<p>4. Scroll Navigation: Users can scroll through content by moving their palm up or down, making it easy to browse long documents and web pages.</p>

<p>5. Swipe Gestures: Horizontal hand movements allow users to switch between tabs, windows, or slides in presentations.</p>

<p><b>Technical Implementation</b></p>
<p>The hand tracking module uses OpenCV for video capture and MediaPipe for landmark detection. The system processes each frame to extract fingertip coordinates, which are then normalized and mapped to screen space.</p>

<p>Gesture detection is based on calculating distances between specific landmarks and tracking hand movement patterns over time. For example, a pinch is detected when the distance between thumb tip and index tip falls below a threshold.</p>

<p><b>Performance Optimization</b></p>
<p>To ensure smooth real-time performance, the system implements several optimizations:</p>
<ul>
<li>Frame rate limiting to 30 FPS</li>
<li>Reduced video resolution (640x480)</li>
<li>Efficient landmark processing</li>
<li>Threading to prevent UI blocking</li>
</ul>

<p><b>Use Cases</b></p>
<p>AirOS is particularly useful in scenarios where traditional input devices are impractical:</p>
<ul>
<li>Presentations and demonstrations</li>
<li>Touchless kiosks and public displays</li>
<li>Accessibility solutions for users with limited mobility</li>
<li>Gaming and entertainment applications</li>
<li>Medical environments requiring sterile interaction</li>
</ul>

<p><b>Future Enhancements</b></p>
<p>Planned improvements include:</p>
<ul>
<li>Multi-hand tracking for advanced gestures</li>
<li>Voice command integration</li>
<li>Machine learning for custom gesture recognition</li>
<li>Support for additional input modalities</li>
<li>Enhanced accuracy and reduced latency</li>
</ul>

<p><b>Conclusion</b></p>
<p>AirOS demonstrates the potential of gesture-based interaction for computer systems. By combining computer vision, machine learning, and intuitive UI design, it provides a natural and engaging way to control digital interfaces without physical contact.</p>

<p><b>Technical Specifications</b></p>
<p>Programming Language: Python 3.11<br>
Computer Vision: MediaPipe, OpenCV<br>
UI Framework: PyQt5<br>
Gesture Detection: Custom algorithms based on landmark analysis<br>
Platform: Windows, Linux (with webcam support)</p>

<p><b>Acknowledgments</b></p>
<p>This project was developed as part of a collaborative effort to explore innovative human-computer interaction methods. Special thanks to the MediaPipe team for providing robust hand tracking solutions.</p>
        """
        
        text_widget.setHtml(document_text)
        scroll.setWidget(text_widget)
        layout.addWidget(scroll)
    
    def create_title_bar(self, title):
        title_bar = QFrame()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet("background-color: #f0f0f0; border-bottom: 1px solid #ccc;")
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(15, 0, 10, 0)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #333; font-size: 14px; font-weight: bold;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(40, 30)
        close_btn.setStyleSheet("""
            QPushButton { background-color: transparent; color: #666; font-size: 18px; border: none; }
            QPushButton:hover { background-color: #e81123; color: white; }
        """)
        close_btn.clicked.connect(self.close)
        title_layout.addWidget(close_btn)
        
        return title_bar


class PowerPointWindow(QWidget):
    """PowerPoint-like presentation app for testing swipe gestures"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: white;")
        self.resize(1000, 700)
        
        from PyQt5.QtWidgets import QApplication
        screen = QApplication.desktop().screenGeometry()
        self.move((screen.width() - 1000) // 2, (screen.height() - 700) // 2)
        
        # Auto-focus this window for keyboard input
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()
        
        self.current_slide = 0
        self.slides = [
            ("AirOS Presentation", "Gesture-Controlled Computing", "#4A90E2"),
            ("What is AirOS?", "• Touchless computer control\n• Hand gesture recognition\n• Real-time interaction", "#E94B3C"),
            ("Key Features", "• Cursor control\n• Click gestures\n• Scroll navigation\n• Swipe between screens", "#50C878"),
            ("Technology Stack", "• Python 3.11\n• MediaPipe\n• OpenCV\n• PyQt5", "#9B59B6"),
            ("Demo Time!", "Try swiping left/right\nto navigate slides →", "#F39C12"),
            ("Thank You!", "Questions?", "#34495E")
        ]
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Title bar
        title_bar = self.create_title_bar("Presentation")
        layout.addWidget(title_bar)
        
        # Slide content
        self.slide_widget = QWidget()
        self.slide_layout = QVBoxLayout(self.slide_widget)
        self.slide_layout.setContentsMargins(60, 80, 60, 80)
        
        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 48px; font-weight: bold; color: white; margin-bottom: 40px;")
        self.slide_layout.addWidget(self.title_label)
        
        self.content_label = QLabel()
        self.content_label.setAlignment(Qt.AlignCenter)
        self.content_label.setStyleSheet("font-size: 28px; color: white; line-height: 1.8;")
        self.content_label.setWordWrap(True)
        self.slide_layout.addWidget(self.content_label)
        
        self.slide_layout.addStretch()
        
        # Slide counter
        self.counter_label = QLabel()
        self.counter_label.setAlignment(Qt.AlignRight)
        self.counter_label.setStyleSheet("font-size: 16px; color: rgba(255,255,255,0.7); padding: 10px;")
        self.slide_layout.addWidget(self.counter_label)
        
        layout.addWidget(self.slide_widget)
        
        # Navigation buttons
        nav_bar = QFrame()
        nav_bar.setFixedHeight(50)
        nav_bar.setStyleSheet("background-color: #2c3e50;")
        nav_layout = QHBoxLayout(nav_bar)
        
        prev_btn = QPushButton("← Previous")
        prev_btn.setStyleSheet("background-color: transparent; color: white; border: none; font-size: 14px;")
        prev_btn.clicked.connect(self.prev_slide)
        prev_btn.setFocusPolicy(Qt.NoFocus)  # Prevent button from stealing focus
        nav_layout.addWidget(prev_btn)
        
        nav_layout.addStretch()
        
        next_btn = QPushButton("Next →")
        next_btn.setStyleSheet("background-color: transparent; color: white; border: none; font-size: 14px;")
        next_btn.clicked.connect(self.next_slide)
        next_btn.setFocusPolicy(Qt.NoFocus)  # Prevent button from stealing focus
        nav_layout.addWidget(next_btn)
        
        layout.addWidget(nav_bar)
        
        self.update_slide()
    
    def update_slide(self):
        title, content, color = self.slides[self.current_slide]
        self.title_label.setText(title)
        self.content_label.setText(content)
        self.slide_widget.setStyleSheet(f"background-color: {color};")
        self.counter_label.setText(f"{self.current_slide + 1} / {len(self.slides)}")
    
    def next_slide(self):
        if self.current_slide < len(self.slides) - 1:
            self.current_slide += 1
            self.update_slide()
    
    def prev_slide(self):
        if self.current_slide > 0:
            self.current_slide -= 1
            self.update_slide()
    
    def keyPressEvent(self, event):
        """Handle keyboard events for slide navigation"""
        from PyQt5.QtCore import Qt
        if event.key() == Qt.Key_Right or event.key() == Qt.Key_Space:
            self.next_slide()
            print("→ Next slide (keyboard)")
        elif event.key() == Qt.Key_Left:
            self.prev_slide()
            print("← Previous slide (keyboard)")
    
    def create_title_bar(self, title):
        title_bar = QFrame()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet("background-color: #2c3e50; border-bottom: 1px solid #34495e;")
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(15, 0, 10, 0)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(40, 30)
        close_btn.setStyleSheet("""
            QPushButton { background-color: transparent; color: white; font-size: 18px; border: none; }
            QPushButton:hover { background-color: #e74c3c; }
        """)
        close_btn.clicked.connect(self.close)
        title_layout.addWidget(close_btn)
        
        return title_bar
