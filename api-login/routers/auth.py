from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from werkzeug.security import check_password_hash
from database import get_db
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
import jwt

# Clave secreta para JWT
SECRET_KEY = "your_secret_jwt_key"
ALGORITHM = "HS256"

router = APIRouter()

# Esquema para las credenciales de inicio de sesión
class LoginCredentials(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login(credentials: LoginCredentials, db: AsyncSession = Depends(get_db)):
    """
    Verifica las credenciales del usuario en la tabla `usr_p360.usuarios` y genera un JWT.
    """
    try:
        # Consulta a la base de datos
        query = text("""
            SELECT identificacion AS id, nombre_usuario AS username, contraseña AS password
            FROM usr_p360.usuarios
            WHERE nombre_usuario = :username
        """)
        result = await db.execute(query, {"username": credentials.username})
        user = result.fetchone()

        # Verificar si el usuario existe
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Verificar la contraseña
        if not check_password_hash(user.password, credentials.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Generar el JWT
        payload = {
            "user_id": user.id,
            "username": user.username,
            "exp": datetime.utcnow() + timedelta(hours=1)  # Expiración de 1 hora
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        # Encabezados anti-caché
        headers = {
            "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
            "Pragma": "no-cache",
            "Expires": "0",
        }

        return JSONResponse(
            content={"token": token, "message": "Login successful"},
            headers=headers
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
