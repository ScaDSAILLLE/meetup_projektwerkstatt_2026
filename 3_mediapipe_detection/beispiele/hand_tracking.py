"""Hand Tracking with MediaPipe.

This example shows how to track hands and detect gestures in real-time.
"""

import cv2
import mediapipe as mp
from typing import List, Tuple, Optional


def get_hand_landmarks(
    image: "cv2.Mat",
    hands: "mp.solutions.hands.Hands",
) -> List["mp.framework.formats.landmark_pb2.NormalizedLandmark"]:
    """Detect hand landmarks in an image.

    Args:
        image: BGR image from OpenCV
        hands: MediaPipe Hands instance

    Returns:
        List of hand landmarks
    """
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    if not results.multi_hand_landmarks:
        return []

    return results.multi_hand_landmarks[0].landmark


def draw_hand_landmarks(
    image: "cv2.Mat",
    landmarks: List["mp.framework.formats.landmark_pb2.NormalizedLandmark"],
) -> "cv2.Mat":
    """Draw hand landmarks on image.

    Args:
        image: BGR image from OpenCV
        landmarks: List of hand landmarks

    Returns:
        Image with drawn landmarks
    """
    h, w, _ = image.shape
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    # Create a blank image for landmarks
    landmark_list = []
    for idx, landmark in enumerate(landmarks):
        cx, cy = int(landmark.x * w), int(landmark.y * h)
        landmark_list.append((cx, cy))

    # Draw connections
    connections = mp_hands.HAND_CONNECTIONS
    for connection in connections:
        start, end = connection
        if start < len(landmark_list) and end < len(landmark_list):
            cv2.line(image, landmark_list[start], landmark_list[end], (0, 255, 0), 2)

    # Draw points
    for point in landmark_list:
        cv2.circle(image, point, 5, (0, 0, 255), -1)

    return image


def detect_gesture(
    landmarks: List["mp.framework.formats.landmark_pb2.NormalizedLandmark"],
) -> Optional[str]:
    """Detect a simple gesture from hand landmarks.

    Args:
        landmarks: List of hand landmarks

    Returns:
        Gesture name or None
    """
    if not landmarks:
        return None

    # Get landmark positions
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    ring_tip = landmarks[16]
    pinky_tip = landmarks[20]

    # Check distances
    def distance(
        a: "mp.framework.formats.landmark_pb2.NormalizedLandmark",
        b: "mp.framework.formats.landmark_pb2.NormalizedLandmark",
    ) -> float:
        return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5

    # Pinch (thumb and index close)
    if distance(thumb_tip, index_tip) < 0.05:
        return "pinch"

    # Open hand (all fingertips far from palm center)
    palm = landmarks[9]
    if (
        distance(index_tip, palm) > 0.2
        and distance(middle_tip, palm) > 0.2
        and distance(ring_tip, palm) > 0.2
        and distance(pinky_tip, palm) > 0.2
    ):
        return "open"

    # Fist (all fingertips close to palm)
    if (
        distance(index_tip, palm) < 0.1
        and distance(middle_tip, palm) < 0.1
        and distance(ring_tip, palm) < 0.1
        and distance(pinky_tip, palm) < 0.1
    ):
        return "fist"

    return None


def main() -> None:
    """Run hand tracking on webcam."""
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5,
    )

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam")
        return

    print("Hand Tracking started. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame")
            break

        landmarks = get_hand_landmarks(frame, hands)

        if landmarks:
            draw_hand_landmarks(frame, landmarks)
            gesture = detect_gesture(landmarks)
            if gesture:
                cv2.putText(
                    frame,
                    f"Gesture: {gesture}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2,
                )

        cv2.imshow("Hand Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
