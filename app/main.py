from fastapi import FastAPI

from app.api.routers.items import router as item_router

app = FastAPI()

app.include_router(item_router, prefix="/items")