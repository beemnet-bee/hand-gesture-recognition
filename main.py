"""
AetherGesture - Standalone Python OpenCV & MediaPipe Desktop App
Recognizes Open Hand, Fist, Thumbs Up, and Victory/Peace in real time.
"""

import cv2
import mediapipe as mp
import time
from gesture_classifier import classify_landmarks

def main():
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    prev_time = time.time()

    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6,
        max_num_hands=1
    ) as hands:
        print("[INFO] Camera stream online. Press 'q' or ESC to exit.")
        
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("[WARNING] Ignoring empty camera frame.")
                continue

            # Flip horizontally for selfie-view display
            image = cv2.flip(image, 1)
            h, w, _ = image.shape

            # Convert BGR to RGB for MediaPipe inference
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image_rgb)

            gesture_name = "SEARCHING"
            confidence = 0.0

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw skeletal connections
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style()
                    )

                    # Classify gesture using geometric heuristics
                    gesture_name, confidence = classify_landmarks(hand_landmarks.landmark)

                    # Draw prominent gesture HUD box
                    cv2.rectangle(image, (30, 30), (450, 100), (10, 15, 25), -1)
                    cv2.rectangle(image, (30, 30), (450, 100), (0, 220, 255), 2)
                    cv2.putText(
                        image,
                        f"{gesture_name} ({confidence*100:.0f}%)",
                        (45, 80),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.2,
                        (255, 255, 255),
                        2,
                        cv2.LINE_AA
                    )

            # Compute and render FPS
            curr_time = time.time()
            fps = 1.0 / max(0.001, (curr_time - prev_time))
            prev_time = curr_time
            cv2.putText(
                image,
                f"FPS: {fps:.1f}",
                (w - 180, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 180),
                2
            )

            cv2.imshow("AetherGesture AI - Desktop Feed", image)
            if cv2.waitKey(5) & 0xFF in (27, ord('q')):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
