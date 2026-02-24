"""Pose Estimation with MediaPipe.

This example shows how to detect body pose in real-time.
"""

import cv2
import mediapipe as mp
from typing import List, Tuple, Optional


def get_pose_landmarks(
    image: "cv2.Mat",
    pose: "mp.solutions.pose.Pose",
) -> List["mp.framework.formats.landmark_pb2.NormalizedLandmark"]:
    """Detect pose landmarks in an image.

    Args:
        image: BGR image from OpenCV
        pose: MediaPipe Pose instance

    Returns:
        List of pose landmarks
    """
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    if not results.pose_landmarks:
        return []

    return results.pose_landmarks.landmark


def draw_pose_landmarks(
    image: "cv2.Mat",
    landmarks: List["mp.framework.formats.landmark_pb2.NormalizedLandmark"],
) -> "cv2.Mat":
    """Draw pose landmarks and connections on image.

    Args:
        image: BGR image from OpenCV
        landmarks: List of pose landmarks

    Returns:
        Image with drawn landmarks
    """
    h, w, _ = image.shape
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    # Draw connections
    connections = mp_pose.POSE_CONNECTIONS
    for connection in connections:
        start, end = connection
        if start < len(landmarks) and end < len(landmarks):
            start_landmark = landmarks[start]
            end_landmark = landmarks[end]

            start_point = (int(start_landmark.x * w), int(start_landmark.y * h))
            end_point = (int(end_landmark.x * w), int(end_landmark.y * h))

            cv2.line(image, start_point, end_point, (0, 255, 0), 2)

    # Draw points
    for landmark in landmarks:
        cx, cy = int(landmark.x * w), int(landmark.y * h)
        cv2.circle(image, (cx, cy), 5, (0, 0, 255), -1)

    return image


def calculate_angle(
    a: "mp.framework.formats.landmark_pb2.NormalizedLandmark",
    b: "mp.framework.formats.landmark_pb2.NormalizedLandmark",
    c: "mp.framework.formats.landmark_pb2.NormalizedLandmark",
) -> float:
    """Calculate angle between three points.

    Args:
        a, b, c: Three landmarks (b is the vertex)

    Returns:
        Angle in degrees
    """
    import math

    a_x, a_y = a.x, a.y
    b_x, b_y = b.x, b.y
    c_x, c_y = c.x, c.y

    angle = math.degrees(
        math.atan2(c_y - b_y, c_x - b_x) - math.atan2(a_y - b_y, a_x - b_x)
    )

    angle = abs(angle)
    if angle > 180:
        angle = 360 - angle

    return angle


def detect_pose_state(
    landmarks: List["mp.framework.formats.landmark_pb2.NormalizedLandmark"],
) -> Optional[str]:
    """Detect simple pose states.

    Args:
        landmarks: List of pose landmarks

    Returns:
        Pose state or None
    """
    if not landmarks:
        return None

    # Get key landmarks
    nose = landmarks[0]
    left_shoulder = landmarks[11]
    right_shoulder = landmarks[12]
    left_hip = landmarks[23]
    right_hip = landmarks[24]

    # Calculate shoulder-hip vertical alignment
    avg_shoulder_y = (left_shoulder.y + right_shoulder.y) / 2
    avg_hip_y = (left_hip.y + right_hip.y) / 2

    # Standing (shoulders above hips)
    if avg_shoulder_y < avg_hip_y - 0.05:
        return "standing"

    # Sitting (shoulders and hips close vertically)
    elif abs(avg_shoulder_y - avg_hip_y) < 0.1:
        return "sitting"

    # Crouching/bent over
    elif nose.y > avg_hip_y + 0.05:
        return "bent_over"

    return "standing"


def main() -> None:
    """Run pose estimation on webcam."""
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(
        static_image_mode=False,
        model_complexity=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam")
        return

    print("Pose Estimation started. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame")
            break

        landmarks = get_pose_landmarks(frame, pose)

        if landmarks:
            draw_pose_landmarks(frame, landmarks)
            state = detect_pose_state(landmarks)
            if state:
                cv2.putText(
                    frame,
                    f"Pose: {state}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2,
                )

        cv2.imshow("Pose Estimation", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
