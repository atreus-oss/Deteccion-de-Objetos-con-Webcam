import cv2
import numpy as np
import requests
import time
import os

# URL de la API para enviar resultados
render_url = os.getenv("RENDER_URL", "http://localhost:8000/api/update")

np.random.seed(20)

class Detector:
    def __init__(self, configPath, modelPath, classesPath):
        self.configPath = configPath
        self.modelPath = modelPath
        self.classesPath = classesPath

        self.net = cv2.dnn_DetectionModel(self.modelPath, self.configPath)
        self.net.setInputSize(320, 320)
        self.net.setInputScale(1.0 / 127.5)
        self.net.setInputMean((127.5, 127.5, 127.5))
        self.net.setInputSwapRB(True)

        self.readClasses()

    def readClasses(self):
        with open(self.classesPath, 'r') as f:
            self.classesList = f.read().splitlines()
        self.colorList = np.random.uniform(low=0, high=255, size=(len(self.classesList), 3))

    def process_frame(self, image):
        startTime = time.time()

        classLabelIDs, confidences, bboxs = self.net.detect(image, confThreshold=0.4)

        bboxs = list(bboxs)
        confidences = list(np.array(confidences).reshape(1, -1)[0])
        confidences = list(map(float, confidences))

        bboxIdx = cv2.dnn.NMSBoxes(bboxs, confidences, score_threshold=0.5, nms_threshold=0.2)

        counts = {
            "person": 0,
            "vehicle": 0,
            "others": 0
        }

        if len(bboxIdx) != 0:
            for i in range(len(bboxIdx)):
                idx = np.squeeze(bboxIdx[i])
                classLabelID = np.squeeze(classLabelIDs[idx])
                classLabel = self.classesList[classLabelID].lower()

                if classLabel == "person":
                    counts["person"] += 1
                elif classLabel in ["car", "truck", "bus", "motorbike", "bicycle"]:
                    counts["vehicle"] += 1
                else:
                    counts["others"] += 1

        endTime = time.time()
        fps = 1 / (endTime - startTime)

        requests.post(render_url, json={
            "person": counts["person"],
            "vehicle": counts["vehicle"],
            "others": counts["others"],
            "fps": round(fps, 2)
        })
