from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# URL de conexión a la base de datos
DATABASE_URL = "postgresql+asyncpg://postgres:jcklqo2134@/postgres?host=/cloudsql/dqh-patrulla-360:southamerica-east1:dqh-patrulla-postgres"

# Crear el motor de la base de datos
engine = create_async_engine(DATABASE_URL, echo=True)

# Crear la fábrica de sesiones
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependencia para obtener la sesión
async def get_db():
    async with async_session() as session:
        yield session
