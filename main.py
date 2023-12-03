from fastapi import FastAPI, WebSocket
from starlette.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocketDisconnect

import controllers.booking
from utils.websocket_manager import ConnectionManager

"""
app entry point start in terminal running: uvicorn main:app --port 8001 --host localhost
"""

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)




app.include_router(controllers.booking.router)
