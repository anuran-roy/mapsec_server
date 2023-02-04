import sys
import os
from dotenv import load_dotenv
from config import BASE_DIR

sys.path.append(str(BASE_DIR))

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.api_router import router as api_router

load_dotenv()
app = FastAPI(
    title="MapSec API Server",
    description="A one-stop tool for scanning your IoT devices connected on your network",
)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/servertest")
async def sayHello(request):
    return {"message": "Hello World"}


app.include_router(api_router)
