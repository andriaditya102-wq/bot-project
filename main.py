from fastapi import FastAPI
from fastapi.responses import FileResponse
import asyncio
import os

app = FastAPI()

# ===== STATE =====
bot_running = False
profit = 0

# ===== BOT LOOP =====
async def bot_loop():
    global profit, bot_running
    while True:
        if bot_running:
            profit += 1
            print(f"Profit: {profit}")
        await asyncio.sleep(2)

# ===== STARTUP =====
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(bot_loop())

# ===== PATH =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ===== ROUTES =====
@app.get("/")
def dashboard():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.post("/start")
def start():
    global bot_running
    bot_running = True
    return {"status": "running"}

@app.post("/stop")
def stop():
    global bot_running
    bot_running = False
    return {"status": "stopped"}

@app.get("/data")
def get_data():
    return {
        "running": bot_running,
        "profit": profit
    }