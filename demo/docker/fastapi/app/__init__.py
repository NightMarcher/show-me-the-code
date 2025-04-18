from logging.config import dictConfig

from fastapi import APIRouter, FastAPI

app = FastAPI(
    title="Demo FastAPI",
)

dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s %(name)s:%(funcName)s:%(lineno)d %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO",
        },
    }
})

root_router = APIRouter()

@root_router.get("/health")
async def check_health():
    return "OK"

@app.on_event("startup")
async def startup():
    app.include_router(root_router) 
    from .api import api_router
    app.include_router(api_router, prefix="/api")
