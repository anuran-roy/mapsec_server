import uuid
from typing import Any, Dict, List, Optional

from tinydb import Query, TinyDB

from db.db import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from models.models import CredentialModel

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
    credType: Optional[str] = "all", db: TinyDB = Depends(get_db)
):
    cred_table = db.table("credentials")
    if credType == "all":
        return cred_table.all()
    else:
        return cred_table.search(Query().credential_type == credType)
