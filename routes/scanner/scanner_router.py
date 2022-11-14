import json
import platform
import time
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

from tinydb import Query, TinyDB

from db.db import get_db
from fastapi import APIRouter, Depends
from models.models import ReportModel, ScanRequestModel
from scripts.check_ports import scan_ports

router = APIRouter(prefix="/scanner", tags=["Vulnerability Scanner"])


@router.post("/new", response_model=ReportModel)
async def scan(details: ScanRequestModel, db: TinyDB = Depends(get_db)) -> Any:
    scan_table = db.table("scans")
    new_id = str(uuid.uuid4())
    request_details = dict(details)
    print(f"Received request details = {request_details}")
    timestamp = str(datetime.now())
    response = {
        "report": {
            "critical": {
                "count": 1,
                "details": [
                    # {
                    #     "type": "credential_leak",
                    #     "description": "Your email account spacecraft.anuran@gmail.com has been mentioned in one or more pastes from data breaches.",
                    #     "timestamp": "2022-09-26T05:25:49.914Z",
                    # },
                    {
                        "type": "credential_leak",
                        "description": "Your email account anuran.roy2020@vitstudent.ac.in has been mentioned in one or more pastes from data breaches.",
                        "timestamp": "2022-09-26T05:25:49.914Z",
                    },
                ],
            },
            "info": {
                "count": 1,
                "details": [
                    {
                        "type": "cpu_usage_high",
                        "description": "The CPU usage has been consistently high since last week. Were you gaming? If not, try looking for apps with high usage that drain battery.",
                        "timestamp": "2022-09-26T05:25:49.914Z",
                    }
                ],
            },
        },
        "id": new_id,
        "name": f"Custom Scan {new_id}",
        "device": platform.node(),
        "description": "Untitled Scan - Scanned on 2022-09-25",
        "timestamp": request_details.get("timestamp", timestamp),
        "target_device": {
            "name": "NA",
            "platform": "Android",
            "type": "phone",
            "metadata": {
                "version": "11.0",
                "baseband": "NA",
                "kernel": "",
                "build_number": "",
            },
        },
    }

    ports_report = scan_ports()
    print(f"{ports_report = }")
    ct = sum([len(list(ports_report[list(ports_report.keys())[0]]))])
    response["report"]["warning"] = {"count": ct, "details": []}

    for i in ports_report:
        for j in ports_report[i]:
            response["report"]["warning"]["details"].append(
                {
                    "type": "port_open",
                    "description": f"Port {j} is open",
                    "timestamp": timestamp,
                }
            )

    # "details": [
    #             {
    #                 "type": "port_open",
    #                 "description": "Port 3090 is open, and it does not match any known settings or defaults for legitimate software/tools",
    #                 "timestamp": "2022-09-26T05:25:49.914Z",
    #             }
    #         ],
    #     }

    print(json.dumps(response, indent=4))
    scan_table.insert(response)
    # time.sleep(2.5)
    print(len(scan_table))
    return response


@router.get("/get_count")
async def get_count(page: Optional[int] = 1, db: TinyDB = Depends(get_db)) -> Any:
    # return {"count": db.count()}
    scan_table = db.table("scans")
    ids = [doc["id"] for doc in scan_table]
    return {"count": len(ids), "ids": ids}


@router.get("/peek/{scan_id}")
async def peek_log(scan_id: str, db: TinyDB = Depends(get_db)):
    scan_table = db.table("scans")
    queryset = scan_table.search(Query().id == scan_id)
    response = (
        dict(queryset[0])
        if len(queryset) > 0
        else {
            "report": {
                "critical": 1,
                "warning": 1,
                "info": 1,
            },
            "id": scan_id,
            "name": f"Custom Scan {scan_id}",
            "description": "Untitled Scan - Scanned on 2022-09-25",
            "timestamp": "2022-09-25T20:01:14.486Z",
        }
    )

    processed_response = (
        response
        | {
            "report": {
                i: response["report"][i]["count"] for i in response["report"].keys()
            }
        }
        if len(queryset) > 0
        else response
    )
    # print(response)
    return processed_response


@router.get("/info/{scan_id}")
async def get_log(scan_id: str, db: TinyDB = Depends(get_db)):
    scan_table = db.table("scans")
    default_response = {
        "report": {
            "critical": {
                "count": 0,
                "details": [
                    # {
                    #     "type": "credential_leak",
                    #     "description": "Your email account spacecraft.anuran@gmail.com has been mentioned in one or more pastes from data breaches.",
                    #     "timestamp": "2022-09-26T05:25:49.914Z",
                    # }
                ],
            },
            "warning": {
                "count": 0,
                "details": [
                    # {
                    #     "type": "port_open",
                    #     "description": "Port 3090 is open, and it does not match any known settings or defaults for legitimate software/tools",
                    #     "timestamp": "2022-09-26T05:25:49.914Z",
                    # }
                ],
            },
            "info": {
                "count": 0,
                "details": [
                    # {
                    #     "type": "cpu_usage_high",
                    #     "description": "The CPU usage has been consistently high since last week. Were you gaming? If not, try looking for apps with high usage that drain battery.",
                    #     "timestamp": "2022-09-26T05:25:49.914Z",
                    # }
                ],
            },
        },
        "id": "NA",  # scan_id,
        "name": "",  # f"Custom Scan {scan_id}",
        "description": "",  # "Untitled Scan - Scanned on 2022-09-25",
        "timestamp": "",  # "2022-09-25T20:01:14.486Z",
        "target_device": {
            "name": "",  # "NA",
            "platform": "",  # "Android",
            "type": "",  # "phone",
            "metadata": {
                "version": "",  # "11.0",
                "baseband": "",  # "NA",
                "kernel": "",
                "build_number": "",
            },
        },
    }

    queryset = scan_table.search(Query().id == scan_id)
    response = queryset[0] if len(queryset) > 0 else default_response
    print(response)
    return response
