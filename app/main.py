from asyncio.log import logger
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import engine, Base
from fastapi import FastAPI
from api.v1.endpoints import auth

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


app.include_router(auth.router)
@app.on_event("startup")
async def startup_event():
    # Create database tables
    async with engine.begin() as conn:
        # Drop all tables
        await conn.run_sync(Base.metadata.drop_all)
        logger.info("Database tables dropped successfully")
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created successfully")