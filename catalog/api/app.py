from fastapi import FastAPI

app = FastAPI(
    title="Catalog API",
    description="Add, delete, and search for items in the catalog.",
    version="1.0.0"
)

# V1 API
from .v1.routes import v1
app.include_router(v1)
