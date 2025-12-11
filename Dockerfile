# Dockerfile
# Usamos una imagen base oficial de Python 3.12, ligera para producción
FROM python:3.12-slim

# Establecer variables de entorno cruciales para Python dentro de Docker
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Crear el directorio de trabajo
WORKDIR /app

# 1. Copiar solo el archivo de requerimientos para aprovechar el cache de Docker
COPY requirements.txt /app/

# 2. Instalar dependencias con opción --no-cache-dir para ahorrar espacio
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copiar el código de la aplicación
# La carpeta app/ contiene app/main.py, app/api, app/core, app/infra
COPY app/ /app/app/

# Exponer el puerto por defecto de Uvicorn/FastAPI
EXPOSE 8000

# Comando de inicio del servidor Uvicorn
# El servidor debe escuchar en 0.0.0.0 para ser accesible desde fuera del contenedor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]