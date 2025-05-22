# para que se ejcute el fastApi: uvicorn main:app --reload --host 0.0.0.0 --port 8000
import os
import requests
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from video_stream import router as video_router
from fastapi.responses import JSONResponse

app = FastAPI()

load_dotenv()
render_url = os.getenv("render_url")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

status = {
    "person": 0,
    "vehicle": 0,
    "others": 0,
    "fps": 0
}

app.include_router(video_router)

@app.get("/")
def root():
    return {"message": "API de detección funcionando. Usa /api/stats para obtener datos."}

@app.get("/api/stats")
def get_stats():
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
    return JSONResponse(content={"url": render_url})


@app.get("/api/datos")
def get_secure_data():
    response = requests.get(render_url)
    data = response.json()
    return data 