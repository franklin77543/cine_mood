from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO: Include routers when Phase 2 starts
# from app.api import movie_api, health_api
# app.include_router(movie_api.router, prefix=settings.API_V1_PREFIX, tags=["movies"])
# app.include_router(health_api.router, prefix=settings.API_V1_PREFIX, tags=["health"])


@app.get("/")
def root():
    return {
        "message": "Welcome to CineMood API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
