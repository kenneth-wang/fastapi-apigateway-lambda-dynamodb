from fastapi import FastAPI
from mangum import Mangum

from app.api.routers.items import router as item_router

app = FastAPI()

app.include_router(item_router, prefix="/items")

# Used for AWS Lambda deployment only
lambda_handler = Mangum(app)
