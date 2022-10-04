from fastapi import APIRouter, Depends
from db.db import get_db
from tinydb import TinyDB, Query
import random
import numpy as np
import time

router = APIRouter(prefix="/analytics", tags=["Analytics API"])


@router.get("/scanhistory")
async def scan_history_analytics(db: TinyDB = Depends(get_db)):
    scan_table = db.table("scans")
    all_timestamps = [dict(i)["timestamp"] for i in scan_table.all()]
    all_counts = [
        sum([i["report"][k]["count"] for k in i["report"].keys()])
        for i in scan_table.all()
    ]
    # choices = [np.random.randint(5, (2,5)) for _ in range(10)]
    print(all_timestamps, all_counts)
    time.sleep(2)
    # while True:
    #     pass
    return [all_timestamps, all_counts]
