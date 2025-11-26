"""
API del Call Center - FastAPI
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rutas import api_router

app = FastAPI(
    title="Call Center API",
    description="API para el sistema de gestión de call center",
    version="1.0.0",
    swagger_ui_parameters={
        "persistAuthorization": True,  # Mantiene el token después de recargar la página
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.get("/", tags=["root"])
def root():
    """Endpoint raíz de la API."""
    return {
        "message": "Bienvenido a la API del Call Center",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }
