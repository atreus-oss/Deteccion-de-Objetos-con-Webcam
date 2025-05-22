import cv2

import numpy as np
from main import render_url
import requests, time

np.random.seed(20)
class Detector:
    def __init__(self, videoPath, configPath, modelPath, classesPath):
        self.videoPath = videoPath
        self.configPath = configPath
        self.modelPath = modelPath
        self.classesPath = classesPath

        ########################################################################################################################################

        self.net = cv2.dnn_DetectionModel(self.modelPath, self.configPath)
        self.net.setInputSize(320,320)
        self.net.setInputScale(1.0/127.5)
        self.net.setInputMean((127.5, 127.5, 127.5))
        self.net.setInputSwapRB(True)

        self.readClasses()

    def readClasses(self):
        with open(self.classesPath, 'r') as f:
            self.classesList = f.read().splitlines()

        self.classesList.insert(0, '__Background__')
        
        self.colorList = np.random.uniform(low=0, high=255, size=(len(self.classesList), 3))

        #print(self.classesList)

    def onVideo(self):
        cap = cv2.VideoCapture(self.videoPath)

        if (cap.isOpened()==False):
            print("Error, no se puede acceder a la cámara")
            return

        (success, image) = cap.read()

        startTime = 0

        while success:
            currentTime = time.time()
            fps = 1/(currentTime - startTime)
            startTime = currentTime
            classLabelIDs, confidences, bboxs = self.net.detect(image, confThreshold=0.4)

            bboxs = list(bboxs)
            confidences = list(np.array(confidences).reshape(1,-1)[0])
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

                    # Clasificación general
                    if classLabel == "person":
                        counts["person"] += 1
                    elif classLabel in ["car", "truck", "bus", "motorbike", "bicycle"]:
                        counts["vehicle"] += 1
                    else:
                        counts["others"] += 1

                    bbox = bboxs[idx]
                    x, y, w, h = bbox
                    classColor = [int(c) for c in self.colorList[classLabelID]]

                    cv2.rectangle(image, (x, y), (x + w, y + h), color=classColor, thickness=1)

                    ########################################################################################################################################

                    lineWidth = min(int(w * 0.3), int(h * 0.3))

                    cv2.line(image, (x,y), (x + lineWidth, y), classColor, thickness=5)
                    cv2.line(image, (x, y), (x, y + lineWidth), classColor, thickness=5)

                    cv2.line(image, (x + w,y), (x + w - lineWidth, y), classColor, thickness=5)
                    cv2.line(image, (x + w,y), (x + w, y + lineWidth), classColor, thickness=5)

                    ########################################################################################################################################

                    cv2.line(image, (x,y + h), (x + lineWidth, y + h), classColor, thickness=5)
                    cv2.line(image, (x,y + h), (x, y + h - lineWidth), classColor, thickness=5)

                    cv2.line(image, (x + w,y + h), (x + w - lineWidth, y + h), classColor, thickness=5)
                    cv2.line(image, (x + w,y + h), (x + w, y + h - lineWidth), classColor, thickness=5)

                    ########################################################################################################################################

                    try:
                        requests.post(render_url, json={
                            "person": counts["person"],
                            "vehicle": counts["vehicle"],
                            "others": counts["others"],
                            "fps": fps
                        })
                    except Exception as e:
                        print("Error enviando datos al API:", e)

                    ########################################################################################################################################

                cv2.putText(image, f"Personas: {counts['person']}", (20, 30), cv2.FONT_HERSHEY_PLAIN, 1.5,
                            (0, 255, 255), 2)
                cv2.putText(image, f"Vehiculos: {counts['vehicle']}", (20, 55), cv2.FONT_HERSHEY_PLAIN, 1.5,
                            (0, 255, 255), 2)
                cv2.putText(image, f"Otros: {counts['others']}", (20, 80), cv2.FONT_HERSHEY_PLAIN, 1.5,
                            (0, 255, 255), 2)
                cv2.putText(image, f"FPS: {int(fps)}", (20, 105), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

            cv2.imshow("Resultado", image)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

            (success, image) = cap.read()
        cap.release()
        cv2.destroyAllWindows()
