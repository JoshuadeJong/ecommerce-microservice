from fastapi import FastAPI

app = FastAPI(
    title="Customer Cart API",
    description="Add or Delete items from a cart, get carts, and get meta data for customer carts.",
    version="1.0.0"
)

# V1 API
from .v1.routes import v1
app.include_router(v1)
