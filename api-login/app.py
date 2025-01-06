from fastapi import FastAPI
from routers import auth
from models.user_model import Base
from database import engine

app = FastAPI()

# Crear tablas si no existen al iniciar la aplicación
@app.on_event("startup")
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Registrar las rutas
app.include_router(auth.router, prefix="/api", tags=["Auth"])


