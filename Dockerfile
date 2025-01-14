# syntax=docker/dockerfile:1.2
FROM python:3.9-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo requirements.txt al contenedor
COPY requirements.txt /app/

# Instalar las dependencias de Python
RUN pip install --upgrade pip setuptools && pip install -r requirements.txt

# Copia las carpetas challenge y data al contenedor
COPY challenge /app/challenge
COPY data /app/data

# Exponer el puerto en el que FastAPI escuchará
EXPOSE 8000

# Comando para ejecutar la aplicación FastAPI en producción con Uvicorn
CMD ["uvicorn", "challenge:application", "--host", "0.0.0.0", "--port", "8000"]