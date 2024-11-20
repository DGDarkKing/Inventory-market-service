# app/main.py

from fastapi import FastAPI

from routes.supply import router as supply_router
from settings import app_settings

app = FastAPI(
    title=app_settings.name,
    debug=app_settings.debug,
)

app.include_router(
    supply_router,
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="localhost",
        port=8001,
        reload=True,
    )
