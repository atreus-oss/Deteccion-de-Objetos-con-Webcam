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
