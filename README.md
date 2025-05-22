[⚠️ Suspicious Content] Monitor de Detección de Objetos con FastAPI y OpenCV

Este proyecto detecta personas, vehículos y otros objetos en tiempo real desde un video o una cámara web, y muestra las estadísticas en una interfaz web utilizando FastAPI como backend.

📁 Estructura del Proyecto

```text
├── backend/
│   │
│   ├── Detector.py
│   │
│   ├── detector_runner.py
│   │
│   ├── main.py
│   │
│   ├── video_stream.py
│   │
│   └── model_data/
│       │
│       ├── frozen_inference_graph.pb
│       │
│       ├── ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt
│       │
│       └── coco.names
│
│   └── test_video/
│       │
│       └── street.mp4
│
├── frontend/
│   │
│   ├── index.html
│   │
│   └── css/
│       │
│       └── index.css
│   └── js/
│       │
│       └── script.js
│
├── requirements.txt
│
└── README.md
```
🚀 Características

Detección de personas, vehículos y otros objetos en tiempo real.

Backend desarrollado con FastAPI.

Visualización de estadísticas en una interfaz web.

Comunicación por API REST entre backend y frontend.

🛠️ Requisitos

Python 3.8+

OpenCV

FastAPI

Uvicorn

⚙️ Instalación

Clona este repositorio:

git clone https://github.com/atreus-oss/Deteccion-de-Objetos-con-Webcam.git

cd Deteccion-de-Objetos-con-Webcam.git

Crea y activa un entorno virtual:

python -m venv venv
# En Windows
venv\Scripts\activate
# En Linux/Mac
source venv/bin/activate

Instala las dependencias:

pip install -r requirements.txt

▶️ Ejecución

1. Iniciar el backend con FastAPI

uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

2. Ejecutar el detector de objetos

python backend/detector_runner.py

3. Abrir el frontend

Abre el archivo frontend/index.html en tu navegador, o usa una extensión como Live Server en VS Code para servir la interfaz.

💭 Endpoints de la API

GET /api/stats: Obtiene las estadísticas actuales.

POST /api/update: Actualiza las estadísticas con nuevos datos.

📊 Notas

Puedes usar la cámara en vivo reemplazando videoPath = 0 en detector_runner.py.

La detección se basa en MobileNet SSD preentrenado sobre COCO.

📄 Licencia

Este proyecto es de uso libre para fines educativos y de desarrollo.