import datetime

from fastapi import APIRouter
from fastapi import Request, Response, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from schemas import ItemIn, ItemOut, SuccessMsg
from database import db_create_item, db_get_items, db_get_single_item, db_delete_item
from starlette.status import HTTP_201_CREATED

router = APIRouter()


@router.post("/api/item", response_model=ItemOut)
async def create_item(request: Request, response: Response, data: ItemIn):
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


@router.get("/api/item/{id}", response_model=ItemOut)
async def get_single_item(id: str):
    res = await db_get_single_item(id)
    if res:
        return res
    raise HTTPException(status_code=404, detail=f"Item of ID:{id} doesn't exist")


@router.delete("/api/item/{id}", response_model=SuccessMsg)
async def delete_item(id: str, request: Request, response: Response):
    res = await db_delete_item(id)
    if res:
        return {"message": "Successfully deleted"}
    raise HTTPException(status_code=404, detail="Delete item failed")
