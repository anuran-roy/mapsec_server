from fastapi import APIRouter
from typing import Any, Optional, Tuple, List, Dict, Union
from models.models import ReportModel, ScanRequestModel
import time

router = APIRouter(prefix="/scanner", tags=["Vulnerability Scanner"])


@router.post("/new", response_model=ReportModel)
async def scan(details: ScanRequestModel) -> Any:
    # print(response)
    print(f"Received request details = {dict(details)}")
    time.sleep(2.5)
    return {
        "report": {
            "critical": {
                "count": 1,
                "details": [
                    {
                        "type": "credential_leak",
                        "description": "Your email account spacecraft.anuran@gmail.com has been mentioned in one or more pastes from data breaches.",
                        "timestamp": "2022-09-26T05:25:49.914Z",
                    }
                ],
            },
            "warning": {
                "count": 1,
                "details": [
                    {
                        "type": "port_open",
                        "description": "Port 3090 is open, and it does not match any known settings or defaults for legitimate software/tools",
                        "timestamp": "2022-09-26T05:25:49.914Z",
                    }
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
        "id": 1,
        "name": "Custom Scan 1",
        "description": "Untitled Scan - Scanned on 2022-09-25",
        "timestamp": "2022-09-25T20:01:14.486Z",
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


@router.get("/peek/{scan_id}")
async def peek_log(scan_id: int):  # , db: TinyDB = Depends(get_db)):
    response = {
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
    print(response)
    return response


@router.get("/info/{scan_id}")
async def get_log(scan_id: int):  # , db: TinyDB = Depends(get_db)):
    response = {
        "report": {
            "critical": {
                "count": 1,
                "details": [
                    {
                        "type": "credential_leak",
                        "description": "Your email account spacecraft.anuran@gmail.com has been mentioned in one or more pastes from data breaches.",
                        "timestamp": "2022-09-26T05:25:49.914Z",
                    }
                ],
            },
            "warning": {
                "count": 1,
                "details": [
                    {
                        "type": "port_open",
                        "description": "Port 3090 is open, and it does not match any known settings or defaults for legitimate software/tools",
                        "timestamp": "2022-09-26T05:25:49.914Z",
                    }
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
        "id": scan_id,
        "name": f"Custom Scan {scan_id}",
        "description": "Untitled Scan - Scanned on 2022-09-25",
        "timestamp": "2022-09-25T20:01:14.486Z",
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
    print(response)
    return response
