# app/main.py

from fastapi import FastAPI

from settings import app_settings
from routes import *

app = FastAPI(
    title=app_settings.name,
    debug=app_settings.debug,
)


app.include_router(
    warehouse_router,
)
app.include_router(
    trading_floor_router,
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="localhost",
        port=8001,
        reload=True,
    )
