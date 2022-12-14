from config import BASE_DIR
import sys

sys.path.append(str(BASE_DIR))

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from routes.api_router import router as api_router

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
