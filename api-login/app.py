# -*- coding: utf-8 -*-
from fastapi import FastAPI
from routers.auth import router as auth_router

app = FastAPI(
    title="API Login",
    description="API para autenticación y generación de tokens JWT",
    version="1.0.0"
)

app.include_router(auth_router, prefix="/api/v1", tags=["Auth"])

@app.get("/")
def root():
    return {"message": "Bienvenido a la API de login"}
