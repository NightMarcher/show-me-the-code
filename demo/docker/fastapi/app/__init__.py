from fastapi import APIRouter, FastAPI

app = FastAPI(
    title="Demo FastAPI",
)

root_router = APIRouter()

@root_router.get("/health")
async def check_health():
    return "OK"

@app.on_event("startup")
async def startup():
    app.include_router(root_router) 
    from .api import api_router
    app.include_router(api_router, prefix="/api") 
