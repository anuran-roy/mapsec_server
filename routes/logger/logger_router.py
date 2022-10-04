from fastapi import APIRouter, Depends, File, Status
from tinydb import TinyDB, Query, Document
from db.db import get_db

router = APIRouter(prefix="/log", tags=["History Logger"])


@router.get("/log/{id}")
def get_log(id: str, db: TinyDB = Depends(get_db)):
    return {}
