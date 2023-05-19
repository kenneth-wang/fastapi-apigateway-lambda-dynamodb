from pydantic import BaseModel

class CreateItemRequest(BaseModel):
    name: str
    category: str
    price: float

class Item(CreateItemRequest):
    id: int
    created_dt: str
    last_updated_dt: str
