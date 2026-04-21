import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
    def extract_landmarks(self, frame):
        """Extract hand landmarks including all fingertips for fist detection"""
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            
            self.mp_draw.draw_landmarks(
                frame, 
                hand_landmarks, 
                self.mp_hands.HAND_CONNECTIONS
            )
            
            # Extract all key landmarks
            thumb_tip = hand_landmarks.landmark[4]
            thumb_ip = hand_landmarks.landmark[3]
            index_tip = hand_landmarks.landmark[8]
            index_pip = hand_landmarks.landmark[6]
            middle_tip = hand_landmarks.landmark[12]
            middle_pip = hand_landmarks.landmark[10]
            ring_tip = hand_landmarks.landmark[16]
            ring_pip = hand_landmarks.landmark[14]
            pinky_tip = hand_landmarks.landmark[20]
            pinky_pip = hand_landmarks.landmark[18]
            wrist = hand_landmarks.landmark[0]
            palm = hand_landmarks.landmark[9]  # Palm center
            
            return {
                "thumb_tip": (int(thumb_tip.x * w), int(thumb_tip.y * h)),
                "thumb_ip": (int(thumb_ip.x * w), int(thumb_ip.y * h)),
                "index_tip": (int(index_tip.x * w), int(index_tip.y * h)),
                "index_pip": (int(index_pip.x * w), int(index_pip.y * h)),
                "middle_tip": (int(middle_tip.x * w), int(middle_tip.y * h)),
                "middle_pip": (int(middle_pip.x * w), int(middle_pip.y * h)),
                "ring_tip": (int(ring_tip.x * w), int(ring_tip.y * h)),
                "ring_pip": (int(ring_pip.x * w), int(ring_pip.y * h)),
                "pinky_tip": (int(pinky_tip.x * w), int(pinky_tip.y * h)),
                "pinky_pip": (int(pinky_pip.x * w), int(pinky_pip.y * h)),
                "wrist": (int(wrist.x * w), int(wrist.y * h)),
                "palm": (int(palm.x * w), int(palm.y * h))
            }
        
        return None
    
    def run(self):
        """Standalone test mode"""
        cap = cv2.VideoCapture(0)
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            landmarks = self.extract_landmarks(frame)
            
            if landmarks:
                cv2.putText(frame, f"Index: {landmarks['index_tip']}", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                cv2.putText(frame, f"Thumb: {landmarks['thumb_tip']}", 
                           (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            cv2.imshow('AirOS - Hand Tracking', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    tracker = HandTracker()
    tracker.run()
