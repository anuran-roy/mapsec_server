import asyncio
import os
import uuid
from typing import Any, Dict, List, Literal, Optional

from tinydb import Query, TinyDB

from db.db import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from models.models import CredentialModel

import aiohttp
from datetime import datetime

router = APIRouter(prefix="/credentials", tags=["Credentials Scanner"])


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_credential(credential: CredentialModel, db: TinyDB = Depends(get_db)):
    cred_table = db.table("credentials")

    credQuery = Query()
    queryset = cred_table.search(
        (credQuery.credential == credential.credential)
        & (credQuery.credential_type == credential.credential_type)
    )

    if len(queryset) > 0:
        return HTTPException(
            status.HTTP_406_NOT_ACCEPTABLE, detail="Entry already exists!"
        )

    cred = dict({**dict(credential), "id": str(uuid.uuid4())})

    cred_table.insert(cred)
    return {"status": status.HTTP_201_CREATED, "created_credential": cred}


@router.get("/", response_model=List[Dict[str, Any]])
async def get_credentials(
    credType: Literal["others", "email", "username", "phone", "domains", "all"] = "all",
    db: TinyDB = Depends(get_db),
):
    cred_table = db.table("credentials")
    if credType == "all":
        return cred_table.all()
    else:
        return cred_table.search(Query().credential_type == credType)


async def search_breachdirectory(
    scope: Literal["auto", "sources", "password", "domain", "dehash"],
    credential: str,
    db: TinyDB,
):
    cred_reports_table: TinyDB.table_class = db.table("credential_reports")
    cred_table: TinyDB.table_class = db.table("credentials")
    leaked_state: bool = False

    report: Dict = {}
    async with aiohttp.ClientSession(
        headers={
            "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
            "X-RapidAPI-Host": os.getenv("RAPIDAPI_BREACHDIRECTORY_HOST_KEY"),
        }
    ) as session:
        async with session.get(
            "https://breachdirectory.p.rapidapi.com/",
            params={
                "func": scope,
                "term": credential,
            },
        ) as request:
            report = await request.json()

    return report


@router.get("/scan", response_model=Dict[str, Any])
def scan_breachdirectory(
    scope: Literal["auto", "sources", "password", "domain", "dehash"],
    credential_type: Literal["others", "email", "username", "phone", "domains"],
    credential: str,
    add_new_credential: Optional[bool] = False,
    db: TinyDB = Depends(get_db),
):
    api_function_arg_map = {
        "email": "auto",
        "username": "auto",
        "sources": "sources",
        "password": "password",
        "domain": "domain",
        "dehash": "dehash",
    }
    cred_reports_table: TinyDB.table_class = db.table("credential_reports")
    cred_table: TinyDB.table_class = db.table("credentials")
    leaked_state: bool = False

    report: Dict = asyncio.run(search_breachdirectory(scope, credential, db))
    leaked_state = len(report["result"]) > 0

    if report["success"]:
        scan_id = str(uuid.uuid4())
        scan_datetime = str(datetime.now())

        credReportQuery = Query()
        queryset = cred_reports_table.search((credReportQuery.key == credential))

        if len(queryset) > 0:
            # Get the existing element
            ele = queryset[0]["scans"]

            # Append scan report to list of scan reports
            cred_reports_table.update(
                {
                    "scans": ele.append(
                        {
                            "scan_id": scan_id,
                            "scan_time": scan_datetime,
                            "scan_scope": scope,
                            "report": report,
                        }
                    )
                },
                credReportQuery.key == key,
            )

            user_query = Query()
            cred_table.update(
                {"leaked": leaked_state, "leaked_date": scan_datetime},
                user_query.credential == credential,
            )

        else:
            if add_new_credential:
                cred_table.insert(
                    dict(
                        {
                            **dict(
                                CredentialModel(
                                    credential=credential,
                                    credential_type=credential_type,
                                    leaked=leaked_state,
                                    leaked_date=scan_datetime,
                                )
                            ),
                            "id": str(uuid.uuid4()),
                        }
                    )
                )

            if len(cred_table.search(Query().credential == credential)) > 0:
                cred_reports_table.insert(
                    {
                        "key": credential,
                        "scans": [
                            {
                                "scan_id": scan_id,
                                "scan_scope": scope,
                                "scan_time": scan_datetime,
                                "report": report,
                            }
                        ],
                    }
                )

    return report


@router.get("/scans", response_model=List[Dict[str, Any]])
def get_credential_scans(db: TinyDB = Depends(get_db)):
    cred_reports_table: TinyDB.table_class = db.table("credential_reports")
    return cred_reports_table.all()


@router.get("/scan/{credential}", response_model=Dict[str, Any])
def get_credential_scans(credential: str, db: TinyDB = Depends(get_db)):
    cred_scans_table: TinyDB.table_class = db.table("credential_reports")
    cred_scans_query = Query()
    queryset = cred_scans_table.search(cred_scans_query.key == credential)

    if len(queryset) > 0:
        return queryset[0]
    else:
        return {}
