from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import asyncio
import os

app = FastAPI()

# Variabel Global
bot_running = False
profit = 0


# Jalankan background task saat aplikasi mulai
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(broadcast_data())

@app.get("/")
async def get_dashboard():
    # Menunjuk langsung ke alamat folder di PythonAnywhere
    index_path = "/home/MuhammadAndriAditya/bot-project/index.html"
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Bot API jalan 🔥, tapi index.html tidak ditemukan di path server"}
@app.get("/start")
def start():
    global bot_running
    bot_running = True
    return {"message": "Bot started"}

@app.get("/stop")
def stop():
    global bot_running
    bot_running = False
    return {"message": "Bot stopped"}
