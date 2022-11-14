import random
import time
from typing import List, Optional, Union

import numpy as np
import pandas as pd
from tinydb import Query, TinyDB

from db.db import get_db
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/analytics", tags=["Analytics API"])


@router.get("/scanhistory/")
async def scan_history_analytics(
    threat_type: Optional[Union[List[str], str]] = "all",
    group_by: Optional[str] = "time",
    freq: Optional[str] = "D",
    db: TinyDB = Depends(get_db),
):
    scan_table = db.table("scans")
    all_timestamps = [dict(i)["timestamp"] for i in scan_table.all()]
    all_counts = [
        sum([i["report"][k]["count"] for k in i["report"].keys()])
        for i in scan_table.all()
    ]
    # choices = [np.random.randint(5, (2,5)) for _ in range(10)]
    # print(all_timestamps, all_counts)
    df = pd.DataFrame({"timestamp": all_timestamps, "count": all_counts})
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df_group = df.groupby(pd.Grouper(key="timestamp", axis=0, freq=freq)).sum()
    df_group["timestamp"] = df_group.index
    # print(df_group)
    time.sleep(2)
    # while True:
    #     pass
    # print("Columns = ", df_group.columns)
    # print([str(i) for i in df_group.index])
    # return [all_timestamps, all_counts]
    return [
        df_group["timestamp"].tolist(),
        [
            df_group["count"].tolist(),
            [i - 2 for i in df_group["count"].tolist()],
            [i + 2 for i in df_group["count"].tolist()],
        ],
    ]
