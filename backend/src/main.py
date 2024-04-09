"""
Main
"""
from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from fastapi_pagination import add_pagination
from fastapi_pagination.utils import disable_installed_extensions_check

from database.db import init_database

from constants import TITLE, DESCRIPTION

from products.views import router as product_router
from user_auth.views import router as user_auth_router
from token_auth.views import router as token_auth_router


tags_metadata = [
    {"name": "User Access", "description": "Access to products with user auth"},
    {"name": "Token Access", "description": "Access to products with token"},
    {"name": "User Auth", "description": "User create and login"},
    {"name": "Token Auth", "description": "Token create and login"}
]


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    await init_database()
    yield

origins = [
    "http://localhost",
    "http://localhost:5173"
]

app = FastAPI(lifespan=lifespan, openapi_tags=tags_metadata, title=TITLE, description=DESCRIPTION)
app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix="/api")
api_router.include_router(product_router)
api_router.include_router(user_auth_router)
api_router.include_router(token_auth_router)

app.include_router(api_router)

add_pagination(app)
disable_installed_extensions_check()

if __name__ == '__main__':
    uvicorn.run(app="main:app")
