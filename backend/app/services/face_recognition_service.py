import os
import logging
from pathlib import Path
from fastapi import UploadFile
import cv2
import face_recognition
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGE_DIR = BASE_DIR / "images"

logger = logging.getLogger(__name__)

def save_person_image(person_id: int, file: UploadFile):
    person_dir = IMAGE_DIR / str(person_id)
    person_dir.mkdir(parents=True, exist_ok=True)
    file_path = person_dir / file.filename

    with file_path.open("wb") as buffer:
        buffer.write(file.file.read())

def recognize_faces(camera_url: str, known_face_encodings, known_face_names):
    cap = cv2.VideoCapture(camera_url)
    if not cap.isOpened():
        logger.error(f"Unable to open camera with URL: {camera_url}")
        raise RuntimeError("Unable to open camera")

    while True:
        ret, frame = cap.read()
        if not ret:
            logger.error("Failed to read frame from camera")
            break

        try:
            # Verify the image type before processing
            if frame.dtype != np.uint8:
                logger.error("Image type is not 8bit")
                continue

            if len(frame.shape) == 2:  # Grayscale image
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
            elif len(frame.shape) == 3 and frame.shape[2] == 3:  # RGB image
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                logger.error("Unsupported image format")
                continue

            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = face_distances.argmin()
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tobytes() + b'\r\n')
        except Exception as e:
            logger.error(f"Error processing frame: {e}")

    cap.release()
