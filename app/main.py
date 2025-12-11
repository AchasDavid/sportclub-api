from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.api.endpoints import router as api_router

# Configuración básica de logging
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Sportclub Beneficios API Intermediaria")

# CORS
origins = [
    "http://localhost:3000", # Puerto común de React
    "http://127.0.0.1:3000",
    "*" # Permite todos los orígenes
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusión de endpoints en la aplicación principal
app.include_router(api_router, prefix="/api/v1")
