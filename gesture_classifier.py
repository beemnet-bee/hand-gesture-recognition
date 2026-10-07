"""
Geometric Heuristic Classifier for Hand Landmarks
"""
import math

def dist2d(p1, p2):
    return math.hypot(p1.x - p2.x, p1.y - p2.y)

def classify_landmarks(landmarks):
    wrist = landmarks[0]
    middle_mcp = landmarks[9]
    scale = max(0.01, dist2d(wrist, middle_mcp))

    # Helper: is standard finger extended
    def is_finger_extended(mcp_idx, pip_idx, tip_idx):
        tip_wrist = dist2d(landmarks[tip_idx], wrist)
        pip_wrist = dist2d(landmarks[pip_idx], wrist)
        return tip_wrist > pip_wrist * 1.15

    index_ext = is_finger_extended(5, 6, 8)
    middle_ext = is_finger_extended(9, 10, 12)
    ring_ext = is_finger_extended(13, 14, 16)
    pinky_ext = is_finger_extended(17, 18, 20)

    thumb_tip = landmarks[4]
    thumb_mcp = landmarks[2]
    thumb_is_up = (thumb_tip.y - thumb_mcp.y) < -0.06

    # 1. Open Hand
    if index_ext and middle_ext and ring_ext and pinky_ext:
        return "OPEN HAND", 0.96

    # 2. Thumbs Up
    if thumb_is_up and not index_ext and not middle_ext and not ring_ext and not pinky_ext:
        return "THUMBS UP", 0.95

    # 3. Fist
    if not index_ext and not middle_ext and not ring_ext and not pinky_ext:
        return "FIST", 0.94

    # 4. Victory / Peace
    if index_ext and middle_ext and not ring_ext and not pinky_ext:
        return "VICTORY / PEACE", 0.97

    # 5. Pointing
    if index_ext and not middle_ext and not ring_ext and not pinky_ext:
        return "POINTING", 0.93

    return "SEARCHING / UNKNOWN", 0.50
