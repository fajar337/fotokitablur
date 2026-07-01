"""
peace_blur.py

Real-time webcam app: detects the "Peace" (V) hand gesture using the
MediaPipe Tasks API (HandLandmarker, NOT the legacy Solutions API).
Whenever a Peace gesture is detected, the entire camera frame is
smoothly blurred (Gaussian blur) using OpenCV. No bounding boxes or
FPS overlay are drawn -- only the smooth blur effect.

Requirements:
    pip install mediapipe opencv-python

Model file:
    Download "hand_landmarker.task" and place it next to this script:
    https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task

Controls:
    q / ESC  -> quit
"""

import math
import os
import sys
import time

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------

MODEL_PATH = "hand_landmarker.task"

CAMERA_INDEX = 0
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

NUM_HANDS = 4
MIN_HAND_DETECTION_CONFIDENCE = 0.6
MIN_HAND_PRESENCE_CONFIDENCE = 0.6
MIN_TRACKING_CONFIDENCE = 0.6

BLUR_KSIZE = 61                  # Gaussian blur kernel size
PINCH_DISTANCE_THRESHOLD = 0.05  # index/middle tip distance to reject "V"
BLUR_SMOOTHING_SPEED = 0.12      # higher = faster transition between sharp/blur

HAND_LANDMARK_INDEX_TIP = 8
HAND_LANDMARK_INDEX_PIP = 6
HAND_LANDMARK_MIDDLE_TIP = 12
HAND_LANDMARK_MIDDLE_PIP = 10
HAND_LANDMARK_RING_TIP = 16
HAND_LANDMARK_RING_PIP = 14
HAND_LANDMARK_PINKY_TIP = 20
HAND_LANDMARK_PINKY_PIP = 18

WINDOW_NAME = "Peace Gesture Face Blur"


# --------------------------------------------------------------------------
# Setup: HandLandmarker (MediaPipe Tasks API)
# --------------------------------------------------------------------------

def create_hand_landmarker(model_path):
    if not os.path.isfile(model_path):
        print(
            f"[ERROR] Model file not found: {model_path}\n"
            "Download it from:\n"
            "https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
            "hand_landmarker/float16/1/hand_landmarker.task"
        )
        sys.exit(1)

    options = vision.HandLandmarkerOptions(
        base_options=python.BaseOptions(model_asset_path=model_path),
        running_mode=vision.RunningMode.VIDEO,
        num_hands=NUM_HANDS,
        min_hand_detection_confidence=MIN_HAND_DETECTION_CONFIDENCE,
        min_hand_presence_confidence=MIN_HAND_PRESENCE_CONFIDENCE,
        min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
    )
    return vision.HandLandmarker.create_from_options(options)


# --------------------------------------------------------------------------
# Gesture helpers
# --------------------------------------------------------------------------

def finger_up(hand_landmarks, tip_idx, pip_idx):
    return hand_landmarks[tip_idx].y < hand_landmarks[pip_idx].y


def landmark_distance(a, b):
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


def detect_peace_gesture(hand_landmarks):
    """Return True if the hand is making a 'V' / Peace sign."""
    index_up = finger_up(hand_landmarks, HAND_LANDMARK_INDEX_TIP, HAND_LANDMARK_INDEX_PIP)
    middle_up = finger_up(hand_landmarks, HAND_LANDMARK_MIDDLE_TIP, HAND_LANDMARK_MIDDLE_PIP)
    ring_up = finger_up(hand_landmarks, HAND_LANDMARK_RING_TIP, HAND_LANDMARK_RING_PIP)
    pinky_up = finger_up(hand_landmarks, HAND_LANDMARK_PINKY_TIP, HAND_LANDMARK_PINKY_PIP)

    is_peace = index_up and middle_up and not ring_up and not pinky_up

    # Reject closed/pinched fingers (looks like a fist, not a V)
    if landmark_distance(
        hand_landmarks[HAND_LANDMARK_INDEX_TIP],
        hand_landmarks[HAND_LANDMARK_MIDDLE_TIP],
    ) < PINCH_DISTANCE_THRESHOLD:
        is_peace = False

    return is_peace


# --------------------------------------------------------------------------
# Blur helper
# --------------------------------------------------------------------------

def blur_frame(frame, alpha, ksize=BLUR_KSIZE):
    """Blend the original frame with a fully blurred version of it.

    `alpha` in [0, 1] controls how much blur is applied (0 = sharp,
    1 = fully blurred), enabling a smooth transition instead of an
    instant on/off switch.
    """
    if alpha <= 0:
        return frame
    if ksize % 2 == 0:
        ksize += 1

    blurred = cv2.GaussianBlur(frame, (ksize, ksize), 0)
    alpha = min(max(alpha, 0.0), 1.0)
    return cv2.addWeighted(blurred, alpha, frame, 1 - alpha, 0)


# --------------------------------------------------------------------------
# Main loop
# --------------------------------------------------------------------------

def main():
    hand_landmarker = create_hand_landmarker(MODEL_PATH)

    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("[ERROR] Could not open webcam.")
        sys.exit(1)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    start_time = time.time()
    blur_alpha = 0.0  # smoothed blur intensity, eases between 0 (sharp) and 1 (blurred)

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                print("[WARN] Failed to read frame from webcam.")
                break

            frame = cv2.flip(frame, 1)

            # Timestamp in ms, must be monotonically increasing for VIDEO mode
            timestamp_ms = int((time.time() - start_time) * 1000)

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

            result = hand_landmarker.detect_for_video(mp_image, timestamp_ms)

            peace_detected = False
            if result.hand_landmarks:
                for hand_landmarks in result.hand_landmarks:
                    if detect_peace_gesture(hand_landmarks):
                        peace_detected = True
                        break

            # Smoothly ease the blur intensity toward its target (0 or 1)
            target_alpha = 1.0 if peace_detected else 0.0
            blur_alpha += (target_alpha - blur_alpha) * BLUR_SMOOTHING_SPEED

            if blur_alpha > 0.01:
                frame = blur_frame(frame, blur_alpha)

            cv2.imshow(WINDOW_NAME, frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q") or key == 27:  # 'q' or ESC
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        hand_landmarker.close()


if __name__ == "__main__":
    main()
