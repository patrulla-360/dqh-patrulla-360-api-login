from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "Usuarios"
    __table_args__ = {"schema": "usr_p360"}  # Especificar el esquema de la tabla

    id = Column("identificacion", Integer, primary_key=True, index=True)
    username = Column("nombre_usuario", String(50), unique=True, nullable=False)
    password = Column("contraseña", String(255), nullable=False)  # Contraseña hasheada
    email = Column("correo_electronico", String(100), nullable=True)
    created_at = Column("created_at", DateTime, default=datetime.utcnow)
