# Usar una imagen base de Python oficial y ligera
FROM python:3.12-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de requerimientos primero para aprovechar cache de Docker
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Exponer el puerto (por defecto 8000, pero Render usa variable PORT)
EXPOSE 8000

# Comando de inicio
# Usamos sh -c para expandir la variable PORT correctamente y permitir fallbacks
CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port ${PORT:-8000}"]
