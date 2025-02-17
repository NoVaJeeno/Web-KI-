# Basis-Image mit Python
FROM python:3.10

# Arbeitsverzeichnis im Container setzen
WORKDIR /app

# Kopiere alle Dateien ins Container-Verzeichnis
COPY . .

# Installiere die notwendigen Python-Abhängigkeiten
RUN pip install --no-cache-dir fastapi uvicorn llama-cpp-python sqlite3

# Exponiere Port 8000 für den Webserver
EXPOSE 8000

# Startbefehl für den FastAPI-Server
CMD ["python", "main.py"]
