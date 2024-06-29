import cv2

def generate_frames(camera_url: str):
    cap = cv2.VideoCapture(camera_url)
    if not cap.isOpened():
        raise RuntimeError("Unable to open camera")

    while True:
        success, frame = cap.read()
        if not success:
            break

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cap.release()
