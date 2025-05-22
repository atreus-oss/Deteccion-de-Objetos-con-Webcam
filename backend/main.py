# Ejecutar FastAPI: uvicorn main:app --host 0.0.0.0 --port 8000

import os
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse

# Cargar variables de entorno desde .env
load_dotenv()
render_url = os.getenv("RENDER_URL")

# Crear instancia de la app
app = FastAPI()

# Habilitar CORS (útil para frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambiar por dominios específicos en producción
    allow_methods=["*"],
    allow_headers=["*"],
)

# Estado actual (memoria local)
status = {
    "person": 0,
    "vehicle": 0,
    "others": 0,
    "fps": 0
}

# Ruta principal
@app.get("/")
def root():
    return {"message": "API de detección funcionando. Usa /api/stats para obtener datos."}

# Obtener estado actual
@app.get("/api/stats")
def get_stats():
    return status

# Modelo para actualizar estado
class StatsUpdate(BaseModel):
    person: int
    vehicle: int
    others: int
    fps: float

# Actualizar estado desde otro componente
@app.post("/api/update")
def update_stats(data: StatsUpdate):
    status.update({
        "person": data.person,
        "vehicle": data.vehicle,
        "others": data.others,
        "fps": round(data.fps, 2)
    })
    return {"message": "Actualizado correctamente"}

# Obtener la URL configurada para el render
@app.get("/api/url")
def get_private_url():
    if not render_url:
        raise HTTPException(status_code=500, detail="Variable RENDER_URL no definida.")
    return JSONResponse(content={"url": render_url})

# Consultar datos externos (ejemplo de fetch remoto)
@app.get("/api/datos")
def get_secure_data():
    if not render_url:
        raise HTTPException(status_code=500, detail="Variable RENDER_URL no definida.")
    
    try:
        response = requests.get(render_url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Error al conectarse a {render_url}: {str(e)}")