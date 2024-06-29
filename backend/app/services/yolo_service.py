import cv2
import os
import logging
from pathlib import Path
from sqlalchemy.orm import Session
from datetime import datetime
from app.crud import create_location
from app.schemas import LocationCreate
from app import models  # Ensure models are imported
import face_recognition
import numpy as np
from fastapi import UploadFile

BASE_DIR = Path(__file__).resolve().parent.parent
YOLO_DIR = BASE_DIR / "yolo"
SCREENSHOT_DIR = BASE_DIR / "screenshots"
IMAGE_DIR = BASE_DIR / "images"

if not SCREENSHOT_DIR.exists():
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger(__name__)

def save_person_image(person_id: int, file: UploadFile):
    person_dir = IMAGE_DIR / str(person_id)
    person_dir.mkdir(parents=True, exist_ok=True)
    file_path = person_dir / file.filename

    with file_path.open("wb") as buffer:
        buffer.write(file.file.read())

def detect_objects_yolo(camera_url: str, db: Session, skip_frames: int = 10, input_size: tuple = (320, 320), latitude: str = "", longitude: str = "", address: str = ""):
    cfg_path = str(YOLO_DIR / "yolov3.cfg")
    weights_path = str(YOLO_DIR / "yolov3.weights")
    coco_path = str(YOLO_DIR / "coco.names")

    if not os.path.exists(cfg_path):
        raise FileNotFoundError(f"YOLO config file not found at {cfg_path}")
    if not os.path.exists(weights_path):
        raise FileNotFoundError(f"YOLO weights file not found at {weights_path}")
    if not os.path.exists(coco_path):
        raise FileNotFoundError(f"COCO names file not found at {coco_path}")

    net = cv2.dnn.readNet(weights_path, cfg_path)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]

    classes = []
    with open(coco_path, "r") as f:
        classes = [line.strip() for line in f.readlines()]

    known_face_encodings = []
    known_face_names = []
    for person in db.query(models.Person).all():
        image_path = str(IMAGE_DIR / str(person.id) / "image.jpg")
        if os.path.exists(image_path):
            image = face_recognition.load_image_file(image_path)
            encoding = face_recognition.face_encodings(image)
            if encoding:
                known_face_encodings.append(encoding[0])
                known_face_names.append(person.name)

    cap = cv2.VideoCapture(camera_url)
    if not cap.isOpened():
        raise RuntimeError("Unable to open camera")

    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        if frame_count % skip_frames != 0:
            continue

        height, width, channels = frame.shape
        blob = cv2.dnn.blobFromImage(frame, 0.00392, input_size, (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = scores.argmax()
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = (0, 255, 0)
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                # If the detected object is a person, perform face recognition
                if label == "person":
                    if x < 0 or y < 0 or x+w > width or y+h > height:
                        continue  # Skip invalid bounding boxes
                    face_frame = frame[y:y + h, x:x + w]
                    if face_frame.size == 0:
                        continue  # Skip empty frames
                    rgb_frame = cv2.cvtColor(face_frame, cv2.COLOR_BGR2RGB)
                    face_locations = face_recognition.face_locations(rgb_frame)
                    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

                    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                        name = "Unknown"

                        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                        best_match_index = np.argmin(face_distances)
                        if matches[best_match_index]:
                            name = known_face_names[best_match_index]

                        cv2.rectangle(frame, (x + left, y + top), (x + right, y + bottom), (0, 0, 255), 2)
                        cv2.rectangle(frame, (x + left, y + bottom - 35), (x + right, y + bottom), (0, 0, 255), cv2.FILLED)
                        font = cv2.FONT_HERSHEY_DUPLEX
                        cv2.putText(frame, name, (x + left + 6, y + bottom - 6), font, 1.0, (255, 255, 255), 1)

                        # Save location and screenshot if a known person is detected
                        if name != "Unknown":
                            timestamp = datetime.utcnow()
                            screenshot_filename = f"{timestamp.strftime('%Y%m%d%H%M%S')}.jpg"
                            screenshot_path = SCREENSHOT_DIR / screenshot_filename
                            cv2.imwrite(str(screenshot_path), frame)

                            location_data = LocationCreate(
                                person_id=best_match_index + 1,  # Adjusted to match the actual person ID
                                latitude=latitude,
                                longitude=longitude,
                                address=address,
                                screenshot=str(screenshot_path)
                            )
                            create_location(db, location_data)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tobytes() + b'\r\n')

    cap.release()
