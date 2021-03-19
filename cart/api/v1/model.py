from typing import Optional
from pydantic import BaseModel, PositiveInt, PositiveFloat


class Item(BaseModel):
    id: str
    name: str
    description: str
    price: PositiveFloat
    quantity: PositiveInt



