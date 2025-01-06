from pydantic import BaseModel, ConfigDict
from typing import Optional

class User(BaseModel):
    id: int
    username: str
    password: Optional[str]  # Generalmente no querrás devolver la contraseña en respuestas
    email: Optional[str]
    created_at: Optional[datetime]

    # Configuración para que Pydantic permita mapear directamente desde un ORM (como SQLAlchemy)
    model_config = ConfigDict(from_attributes=True)
