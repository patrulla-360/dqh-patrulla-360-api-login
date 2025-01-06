from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from werkzeug.security import check_password_hash
from database import get_db
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta

# Clave secreta para JWT
SECRET_KEY = "your_secret_jwt_key"
ALGORITHM = "HS256"

# Crear el enrutador
router = APIRouter()

# Esquema para las credenciales de inicio de sesión
class LoginCredentials(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login(credentials: LoginCredentials, db: AsyncSession = Depends(get_db)):
    """
    Verifica las credenciales del usuario y genera un JWT si son válidas.
    """
    try:
        # Consulta para obtener el usuario
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

        # Validar la contraseña
        if not check_password_hash(user.password, credentials.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Generar JWT
        payload = {
            "user_id": user.id,
            "username": user.username,
            "exp": datetime.utcnow() + timedelta(hours=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return {"token": token, "message": "Login successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during login: {e}")
