# Imagen base
FROM python:3.9-slim

# Directorio de trabajo
WORKDIR /app

# Copiar los archivos de dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY . .

# Comando para ejecutar la API
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
