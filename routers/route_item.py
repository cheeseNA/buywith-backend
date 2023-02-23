import datetime

from fastapi import APIRouter
from fastapi import Request, Response, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from schemas import ItemIn, ItemOut
from database import db_create_item, db_get_items
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


@router.get("/api/item", response_model=list[ItemOut])
async def get_items(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, gt=0, le=100),
):
    res = await db_get_items(skip, limit)
    return res
