import cv2
import time
import requests
import numpy as np
import os
from ultralytics import YOLO

# URL del backend FastAPI (Render o local)
render_url = os.getenv("RENDER_URL", "http://localhost:8000/api/update")

class Detector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

        #Cargar clases de COCO (nombre de objetos)
        self.classesList = self.model.names
        self.colorList = np.random.uniform(0, 255, size=(len(self.classesList), 3))

    def process_frame(self, frame):
        start_time = time.time()

        results = self.model(frame, stream=False)[0]

        counts = {
            "person": 0,
            "vehicle": 0,
            "others": 0
        }

        for r in results.boxes:
            class_id = int(r.cls[0])
            conf = float(r.conf[0])
            x1, y1, x2, y2 = map(int, r.xyxy[0])

            label = self.classesList[class_id].lower()
            color = [int(c) for c in self.colorList[class_id]]
            w, h = x2 - x1, y2 - y1

            # Clasificación básica
            if label == "person":
                counts["person"] += 1
            elif label in ["car", "truck", "bus", "motorbike", "bicycle"]:
                counts["vehicle"] += 1
            else:
                counts["others"] += 1

            # Dibujar rectángulo
            cv2.rectangle(frame, (x1, y1), (x2, y2), color=color, thickness=2)

            # Etiqueta
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # Esquinas decorativas
            lw = min(int(w * 0.3), int(h * 0.3))
            # Sup Izq
            cv2.line(frame, (x1, y1), (x1 + lw, y1), color, 4)
            cv2.line(frame, (x1, y1), (x1, y1 + lw), color, 4)
            # Sup Der
            cv2.line(frame, (x2, y1), (x2 - lw, y1), color, 4)
            cv2.line(frame, (x2, y1), (x2, y1 + lw), color, 4)
            # Inf Izq
            cv2.line(frame, (x1, y2), (x1 + lw, y2), color, 4)
            cv2.line(frame, (x1, y2), (x1, y2 - lw), color, 4)
            # Inf Der
            cv2.line(frame, (x2, y2), (x2 - lw, y2), color, 4)
            cv2.line(frame, (x2, y2), (x2, y2 - lw), color, 4)

        end_time = time.time()
        fps = 1 / (end_time - start_time)

        # Enviar datos al backend
        try:
            requests.post(render_url, json={
                "person": counts["person"],
                "vehicle": counts["vehicle"],
                "others": counts["others"],
                "fps": round(fps, 2)
            })
        except Exception as e:
            print("[ERROR] No se pudo enviar a la API:", e)

        return {
            "person": counts["person"],
            "vehicle": counts["vehicle"],
            "others": counts["others"],
            "fps": round(fps, 2)
        }
