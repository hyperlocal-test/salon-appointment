from fastapi import FastAPI
from .routers import api_router

app = FastAPI(title="Hyperlocal - API Integration",
    version="0.2.0",
    servers=[
        {
            "url": "http://localhost:8081/",
            "description": "Hyperlocal Local"
        }
    ]
)

app.include_router(api_router, prefix="/api/v1")