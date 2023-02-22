from datetime import datetime
from enum import Enum

from pydantic import BaseModel, HttpUrl


class SuccessMsg(BaseModel):
    message: str


class State(str, Enum):
    open = "open"
    gathered = "gathered"
    close = "close"
    stop = "stop"


class UserId(BaseModel):
    id: str


class ChatId(BaseModel):
    id: str


class ItemInDB(BaseModel):
    id: str
    title: str
    description: str
    url: HttpUrl
    associate_url: HttpUrl | None = None
    published_datetime: datetime
    until_datetime: datetime | None = None
    closed_datetime: datetime | None = None
    state: State
    num_persons_required: int
    joining_person: list[UserId]
    is_for_unit: bool
    chat: ChatId


class ItemIn(BaseModel):
    title: str
    description: str
    url: HttpUrl
    until_datetime: datetime | None = None
    num_persons_required: int
    is_for_unit: bool


class ItemOut(BaseModel):
    id: str
    title: str
    description: str
    url: HttpUrl
    associate_url: HttpUrl | None = None
    published_datetime: datetime
    until_datetime: datetime | None = None
    closed_datetime: datetime | None = None
    state: State
    num_persons_required: int
    joining_person: list[UserId]
    is_for_unit: bool
    chat: ChatId


class Csrf(BaseModel):
    csrf_token: str
