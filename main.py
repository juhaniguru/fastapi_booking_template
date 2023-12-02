

from fastapi import  FastAPI
from starlette.middleware.cors import CORSMiddleware

import controllers.booking

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(controllers.booking.router)

