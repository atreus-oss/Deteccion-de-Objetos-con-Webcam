import os
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

# Cargar variables de entorno
load_dotenv()
render_url = os.getenv("RENDER_URL")

# Crear app FastAPI
app = FastAPI()

# Activar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta a carpeta del frontend
frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend')

# Montar rutas estáticas (css, js) después de definir el path
app.mount("/css", StaticFiles(directory=os.path.join(frontend_path, "css")), name="css")
app.mount("/js", StaticFiles(directory=os.path.join(frontend_path, "js")), name="js")

# Servir index.html desde /
@app.get("/")
async def root():
    return FileResponse(os.path.join(frontend_path, "index.html"))

# Estado simulado
status = {
    "person": 0,
    "vehicle": 0,
    "others": 0,
    "fps": 0
}

@app.get("/api/stats")
def stats():
    return status

class StatsUpdate(BaseModel):
    person: int
    vehicle: int
    others: int
    fps: float

@app.post("/api/update")
def update_stats(data: StatsUpdate):
    status.update({
        "person": data.person,
        "vehicle": data.vehicle,
        "others": data.others,
        "fps": round(data.fps, 2)
    })
    return {"message": "Actualizado correctamente"}

@app.get("/api/url")
def get_private_url():
    if not render_url:
        raise HTTPException(status_code=500, detail="Variable RENDER_URL no definida.")
    return JSONResponse(content={"url": render_url})

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
