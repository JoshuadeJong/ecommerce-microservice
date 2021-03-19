from typing import Optional, List
from pydantic import BaseModel, PositiveInt, PositiveFloat


class Item(BaseModel):
    name: str
    description: str
    price: PositiveFloat
    stock: PositiveInt
