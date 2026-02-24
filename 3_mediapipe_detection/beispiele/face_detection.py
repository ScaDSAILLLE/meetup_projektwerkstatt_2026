"""Simple Face Detection with MediaPipe.

This example shows how to detect faces in real-time using the webcam.
"""

import cv2
import mediapipe as mp
from typing import List, Tuple


def detect_faces(
    image: "cv2.Mat",
    face_detection: "mp.solutions.face_detection.FaceDetection",
) -> List[Tuple[int, int, int, int]]:
    """Detect faces in an image.

    Args:
        image: BGR image from OpenCV
        face_detection: MediaPipe Face Detection instance

    Returns:
        List of bounding boxes as (x, y, width, height)
    """
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_detection.process(image_rgb)

    if not results.detections:
        return []

    h, w, _ = image.shape
    boxes = []

    for detection in results.detections:
        bbox = detection.location_data.relative_bounding_box
        x = int(bbox.xmin * w)
        y = int(bbox.ymin * h)
        width = int(bbox.width * w)
        height = int(bbox.height * h)
        boxes.append((x, y, width, height))

    return boxes


def draw_faces(image: "cv2.Mat", boxes: List[Tuple[int, int, int, int]]) -> "cv2.Mat":
    """Draw bounding boxes around faces.

    Args:
        image: BGR image from OpenCV
        boxes: List of bounding boxes

    Returns:
        Image with drawn boxes
    """
    for x, y, w, h in boxes:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return image


def main() -> None:
    """Run face detection on webcam."""
    mp_face_detection = mp.solutions.face_detection
    face_detection = mp_face_detection.FaceDetection(
        model_selection=0, min_detection_confidence=0.5
    )

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam")
        return

    print("Face Detection started. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame")
            break

        boxes = detect_faces(frame, face_detection)
        draw_faces(frame, boxes)

        cv2.imshow("Face Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
