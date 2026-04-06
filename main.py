from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import asyncio
import os

app = FastAPI()

# Variabel Global
bot_running = False
profit = 0
clients = set()

# Fungsi untuk mengirim data ke semua koneksi WebSocket
async def broadcast_data():
    global profit, bot_running
    while True:
        if bot_running:
            profit += 1
            data = {
                "log": "Bot sedang jalan...",
                "profit": profit
            }
            # Kirim ke semua client yang terhubung
            if clients:
                await asyncio.gather(
                    *[client.send_json(data) for client in clients],
                    return_exceptions=True
                )
        await asyncio.sleep(2)

# Jalankan background task saat aplikasi mulai
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(broadcast_data())

@app.get("/")
async def get_dashboard():
    # Menampilkan file index.html sebagai tampilan utama
    if os.path.exists("index.html"):
        return FileResponse("index.html")
    return {"message": "Bot API jalan 🔥, tapi index.html tidak ditemukan"}

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

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    try:
        while True:
            await websocket.receive_text() # Tetap jaga koneksi
    except WebSocketDisconnect:
        clients.remove(websocket)