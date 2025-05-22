import cv2
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter()


def gen_frames():
    cap = cv2.VideoCapture(0)  # Usa 0 para la webcam integrada o externa
    if not cap.isOpened():
        raise RuntimeError("No se pudo acceder a la cámara.")

    while True:
        success, frame = cap.read()
        if not success:
            break

camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Procesar el frame si quieres (detección)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.get("/video_feed")
def video_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")




