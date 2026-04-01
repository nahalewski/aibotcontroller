import asyncio
import json
import base64
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import List, Dict

from services.coordinator import CoordinatorService

app = FastAPI()
coordinator = CoordinatorService()

# CORS for Electron/React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                pass

manager = ConnectionManager()

# Set up coordinator callback to broadcast frames
def on_frame_recorded(image_b64: str, metrics: Dict):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    msg = json.dumps({
        "type": "frame_update",
        "image": image_b64,
        "metrics": metrics
    })
    # Since coordinator runs in a separate thread, we need to bridge to asyncio
    asyncio.run_coroutine_threadsafe(manager.broadcast(msg), main_loop)

coordinator.on_frame_callback = on_frame_recorded

@app.get("/status")
def get_status():
    return coordinator.get_status()

@app.get("/windows")
def get_windows():
    return coordinator.capture.get_windows()

@app.post("/select_window")
def select_window(config: Dict):
    title = config.get("title")
    success = coordinator.capture.select_window(title)
    return {"success": success}

@app.post("/start")
def start_loop(config: Dict):
    coordinator.start(config)
    return {"success": True}

@app.post("/stop")
def stop_loop():
    coordinator.stop()
    return {"success": True}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Just keep the connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import threading
    global main_loop
    main_loop = asyncio.get_event_loop()
    uvicorn.run(app, host="0.0.0.0", port=8000)
