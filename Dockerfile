# Usa una imagen base oficial de Python
FROM python:3.10-slim

# Establece un directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . /app

# Instala las herramientas necesarias para construir dependencias (si es necesario)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Crea y activa un entorno virtual para las dependencias
RUN python -m venv venv

# Activa el entorno virtual y actualiza pip
RUN . venv/bin/activate && pip install --upgrade pip

# Instala las dependencias del proyecto y Sentry SDK
RUN . venv/bin/activate && pip install -r requirements.txt && pip install sentry-sdk

# Expone el puerto donde correrá la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["sh", "-c", ". venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8000"]
