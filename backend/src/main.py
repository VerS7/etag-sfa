"""
Main
"""
from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI, staticfiles, APIRouter
from fastapi.responses import RedirectResponse
from fastapi.requests import Request

from database.db import init_database

from products.views import router as product_router
from auth.views import router as user_auth_router


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    await init_database()
    yield

app = FastAPI(lifespan=lifespan)

api_router = APIRouter(prefix="/api")
api_router.include_router(product_router)
api_router.include_router(user_auth_router)

app.include_router(api_router)

# Test frontend
# ---------------------
app.mount("/home", staticfiles.StaticFiles(directory="../../frontend/dist"), name="home")
app.mount("/assets", staticfiles.StaticFiles(directory="../../frontend/dist/assets"), name="assets")


@app.get("/")
def homepage(request: Request):
    return RedirectResponse("/home/index.html")
# ---------------------


# Test endpoint
# ---------------------
@app.get("/test")
async def api_test():
    return {"test": "Test Complete!"}
# ---------------------


if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=True)