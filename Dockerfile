# Imagen de Python ligera
FROM python:3.12-slim

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Instalar primero las dependencias para aprovechar la cache de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el codigo de la aplicacion
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
