from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas import SuccessMsg

from routers import route_item

app = FastAPI()
app.include_router(route_item.router)

origins = ["https://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=SuccessMsg)
def read_root():
    return {"message": "Welcome to Fast API"}
