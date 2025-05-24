# detector_runner_yolo.py
from ultralytics import YOLO
import cv2
import requests
import os
from dotenv import load_dotenv

load_dotenv()

RENDER_URL = os.getenv("RENDER_URL", "http://localhost:8000/api/update")


def main():
    model_path = os.getenv("YOLO_MODEL_PATH", "yolov8n.pt")
    model = YOLO(model_path)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("No se pudo abrir la cámara")
        return

    print("Cámara abierta correctamente. Presiona 'q' para salir")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model.predict(source=frame, imgsz=640, conf=0.4, verbose=False)[0]

        counts = {"person": 0, "vehicle": 0, "others": 0}

        for box in results.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id].lower()
            conf = float(box.conf[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Clasificación personalizada
            if label == "person":
                counts["person"] += 1
            elif label in ["car", "truck", "bus", "motorbike", "bicycle"]:
                counts["vehicle"] += 1
            else:
                counts["others"] += 1

            color = (0, 255, 0) if label == "person" else (255, 255, 0) if label in ["car", "truck", "bus", "motorbike",
                                                                                     "bicycle"] else (200, 0, 255)

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # Esquinas decorativas
            lw = min(int((x2 - x1) * 0.3), int((y2 - y1) * 0.3))
            cv2.line(frame, (x1, y1), (x1 + lw, y1), color, 3)
            cv2.line(frame, (x1, y1), (x1, y1 + lw), color, 3)
            cv2.line(frame, (x2, y1), (x2 - lw, y1), color, 3)
            cv2.line(frame, (x2, y1), (x2, y1 + lw), color, 3)
            cv2.line(frame, (x1, y2), (x1 + lw, y2), color, 3)
            cv2.line(frame, (x1, y2), (x1, y2 - lw), color, 3)
            cv2.line(frame, (x2, y2), (x2 - lw, y2), color, 3)
            cv2.line(frame, (x2, y2), (x2, y2 - lw), color, 3)

        fps = cap.get(cv2.CAP_PROP_FPS) or 0

        # Mostrar en pantalla
        cv2.putText(frame, f"Personas: {counts['person']}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(frame, f"Vehiculos: {counts['vehicle']}", (10, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(frame, f"Otros: {counts['others']}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        try:
            requests.post(RENDER_URL, json={
                "person": counts["person"],
                "vehicle": counts["vehicle"],
                "others": counts["others"],
                "fps": round(fps, 2)
            })
        except Exception as e:
            print("Error al enviar datos a la API:", e)

        cv2.imshow("Detección YOLOv8", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
