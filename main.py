from typing import List, Optional
import databases
import sqlalchemy
from fastapi import FastAPI
import ormar

from db import database, engine, metadata
from downloadFilesApi import video_router

app = FastAPI()

# ORM

app.state.database = database

app.include_router(video_router)

# metadata.create_all(engine)


# ORM quit
@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()