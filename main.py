from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import sqlite3
import os
from llama_cpp import Llama  # Lädt ein lokales LLM-Modell

app = FastAPI()

# SQLite Datenbank einrichten
DB_FILE = "chat.db"
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        message TEXT
    )
""")
conn.commit()

# Lade ein lokales LLM-Modell (Pfad anpassen)
MODEL_PATH = "models/llama-7b.gguf"
llm = Llama(model_path=MODEL_PATH)

@app.get("/", response_class=HTMLResponse)
async def home():
    return open("index.html", "r").read()

@app.post("/chat")
async def chat(message: dict):
    user_message = message["message"]
    cursor.execute("INSERT INTO messages (user, message) VALUES (?, ?)", ("User", user_message))
    conn.commit()

    response = llm(user_message)
    ai_response = response["choices"][0]["text"]

    cursor.execute("INSERT INTO messages (user, message) VALUES (?, ?)", ("KI", ai_response))
    conn.commit()

    return {"response": ai_response}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return {"message": f"Datei {file.filename} hochgeladen"}

if __name__ == "__main__":
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    os.makedirs("models", exist_ok=True)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
