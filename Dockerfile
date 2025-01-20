# Usa una imagen base oficial de Python
FROM python:3.10-slim

# Establece un directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . /app

# Instala las herramientas necesarias para crear el entorno virtual y las dependencias
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-venv \
    libpython3-dev \
    && rm -rf /var/lib/apt/lists/*

# Crea y activa un entorno virtual para las dependencias
RUN python -m venv venv

# Activa el entorno virtual y actualiza pip
RUN . venv/bin/activate && pip install --upgrade pip

# Instala las dependencias del proyecto y Sentry SDK
RUN . venv/bin/activate && pip install -r requirements.txt && pip install sentry-sdk

# Expone el puerto donde correrá la aplicación
EXPOSE 8000

# Cambia CMD para garantizar que el entorno virtual se active correctamente cuando el contenedor se ejecute.
CMD ["/bin/bash", "-c", "source venv/bin/activate && exec uvicorn main:app --host 0.0.0.0 --port 8000"]
