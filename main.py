from fastapi import FastAPI, WebSocket
import threading
import time
import asyncio

app = FastAPI()

bot_running = False
clients = []

def bot_loop():
    global bot_running
    profit = 0

    while bot_running:
        profit += 1

        data = {
            "log": "Bot sedang jalan...",
            "profit": profit
        }

        print(data)

        for client in clients:
            try:
                asyncio.run(client.send_json(data))
            except:
                pass

        time.sleep(2)

@app.get("/")
def home():
    return {"message": "Bot API jalan 🔥"}

@app.get("/start")
def start():
    global bot_running
    if not bot_running:
        bot_running = True
        threading.Thread(target=bot_loop).start()
        return {"message": "Bot started"}
    return {"message": "Bot already running"}

@app.get("/stop")
def stop():
    global bot_running
    bot_running = False
    return {"message": "Bot stopped"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        clients.remove(websocket)