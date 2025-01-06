from fastapi import FastAPI
from routers.auth import router as auth_router  # Importar las rutas de autenticación

app = FastAPI(
    title="API Login",
    description="API para autenticación y generación de tokens JWT",
    version="1.0.0"
)

# Registrar rutas
app.include_router(auth_router, prefix="/api/v1", tags=["Auth"])

@app.get("/")
def root():
    return {"message": "Bienvenido a la API de login"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
