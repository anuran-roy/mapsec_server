from tinydb import Document, Query, TinyDB

from db.db import get_db
from fastapi import APIRouter, Depends, File, Status

router = APIRouter(prefix="/log", tags=["History Logger"])


@router.get("/log/{log_type}")
def get_log(log_type: str = "all", id: str = "", db: TinyDB = Depends(get_db)):
    return {}
