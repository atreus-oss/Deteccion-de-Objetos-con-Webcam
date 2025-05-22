import os
from Detector import *

def main():
    videoPath = os.path.abspath("test_video/street.mp4")
    configPath = os.path.abspath("model_data/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
    modelPath = os.path.abspath("model_data/frozen_inference_graph.pb")
    classesPath = os.path.abspath("model_data/coco.names")

    print(f"videoPath = {videoPath}")
    print(f"configPath = {configPath}")
    print(f"modelPath = {modelPath}")
    print(f"classesPath = {classesPath}")

    detector = Detector(videoPath, configPath, modelPath, classesPath)
    detector.onVideo()

if __name__ == '__main__':
    main()
