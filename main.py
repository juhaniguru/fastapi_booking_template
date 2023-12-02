from fastapi import FastAPI, WebSocket
from starlette.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocketDisconnect

import controllers.booking
from utils.socket_manager import ConnectionManager

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(data, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


app.include_router(controllers.booking.router)
