"""
Main
"""
from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI, APIRouter

from fastapi_pagination import add_pagination
from fastapi_pagination.utils import disable_installed_extensions_check

from database.db import init_database

from products.views import router as product_router
from user_auth.views import router as user_auth_router
from token_auth.views import router as token_auth_router


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    await init_database()
    yield

app = FastAPI(lifespan=lifespan)

api_router = APIRouter(prefix="/api")
api_router.include_router(product_router)
api_router.include_router(user_auth_router)
api_router.include_router(token_auth_router)

app.include_router(api_router)

add_pagination(app)
disable_installed_extensions_check()


if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=True)