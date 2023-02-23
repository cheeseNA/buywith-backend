import datetime

from fastapi import APIRouter
from fastapi import Request, Response, HTTPException
from fastapi.encoders import jsonable_encoder
from schemas import ItemIn, ItemOut
from database import db_create_item
from starlette.status import HTTP_201_CREATED

router = APIRouter()


@router.post("/api/item", response_model=ItemOut)
async def create_todo(request: Request, response: Response, data: ItemIn):
    item = jsonable_encoder(data)
    item.update(
        {
            "published_datetime": datetime.datetime.utcnow(),
            "state": "open",
            "joining_person": [],
            "chat": {"id": "-1"},
        }
    )
    res = await db_create_item(item)
    response.status_code = HTTP_201_CREATED
    if res:
        return res
    raise HTTPException(status_code=404, detail="Create item failed")
