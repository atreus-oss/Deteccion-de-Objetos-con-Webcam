from Detector import Detector
import cv2, os
from dotenv import load_dotenv

load_dotenv()

def main():
    # Configuraciones del modelo (cargadas desde .env)
    configPath = os.getenv("MODEL_CONFIG_PATH")
    modelPath = os.getenv("MODEL_WEIGHTS_PATH")
    classesPath = os.getenv("MODEL_CLASSES_PATH")

    # Validar rutas
    if not all([configPath, modelPath, classesPath]):
        print("Error: Faltan rutas del modelo en el archivo .env")
        return

    detector = Detector(configPath, modelPath, classesPath)

    cap = cv2.VideoCapture(0)  # Cámara local

    if not cap.isOpened():
        print("No se pudo abrir la cámara")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = detector.process_frame(frame)

        # Mostrar los resultados localmente (opcional)
        cv2.putText(frame, f"Personas: {results['person']}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
        cv2.putText(frame, f"Vehiculos: {results['vehicle']}", (10, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
        cv2.putText(frame, f"Otros: {results['others']}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
        cv2.putText(frame, f"FPS: {results['fps']}", (10, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

        cv2.imshow("Detección", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
