import os
import uuid
from typing import Any, Dict, List, Optional

from tinydb import TinyDB

from db.db import get_db, get_log_db
from fastapi import APIRouter, Depends, File, status
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from main import BASE_DIR

router = APIRouter(prefix="/sync", tags=["Sync API"])

os.makedirs(str(BASE_DIR / "sync_data"), exist_ok=True)


@router.post(
    "/from_file", response_model=Dict[str, Any], status_code=status.HTTP_202_ACCEPTED
)
async def sync_data_from_file(
    uploadFile: bytes = File(...),
    db: TinyDB = Depends(get_db),
    log_db: TinyDB = Depends(get_log_db),
):
    try:
        fileName = f"{str(uuid.uuid4())}.json"
        filePath = BASE_DIR / "sync_data" / fileName

        with open(str(filePath), "wb") as target_file:
            target_file.write(uploadFile)

        source_db = TinyDB(filePath)

        ct = 0
        # db_len = len(db)

        for table in source_db.tables():
            target_table = db.table(table)
            elements_to_transfer = source_db.table(table).all()
            ct += len(elements_to_transfer)

            for element in elements_to_transfer:
                target_table.insert(dict(element))

        return {
            "status": status.HTTP_202_ACCEPTED,
            "message": f"{ct} elements synced to PC.",
        }
    except Exception as e:
        print(e)
        return HTTPException(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something broke inside :( Check server logs for more details",
        )


# @router.get("/to_file", status_code=status.HTTP_200_OK)
# async def export_file(db: TinyDB = Depends(get_db), log_db: TinyDB = Depends(get_log_db)):
#     def iter_file():
#         with open(str(BASE_DIR / "db.json"), "rb") as out_file:
#             yield from out_file

#     return StreamingResponse(iter_file(), media_type="application/json")


# NOTE: The below endpoint does the exact same thing
@router.get("/to_file", status_code=status.HTTP_200_OK, response_class=FileResponse)
async def export_file(
    db: TinyDB = Depends(get_db), log_db: TinyDB = Depends(get_log_db)
):
    headers = {"Access-Control-Expose-Headers": "Content-Disposition"}
    return FileResponse(str(BASE_DIR / "db.json"), filename="db.json", headers=headers)
