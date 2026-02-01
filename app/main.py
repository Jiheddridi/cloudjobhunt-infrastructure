"""
CloudJobHunt API - Main Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db
from app.api import auth, users, jobs


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    
    app = FastAPI(
        title=settings.APP_NAME,
        description="API for CloudJobHunt - Job Search Application",
        version="1.0.0",
        debug=settings.DEBUG,
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Initialize database
    init_db()
    
    # Include routers
    app.include_router(auth.router, prefix=settings.API_V1_PREFIX, tags=["Authentication"])
    app.include_router(users.router, prefix=settings.API_V1_PREFIX, tags=["Users"])
    app.include_router(jobs.router, prefix=settings.API_V1_PREFIX, tags=["Jobs"])
    
    @app.get("/")
    async def root():
        return {"message": "CloudJobHunt API", "version": "1.0.0"}
    
    @app.get("/health")
    async def health():
        return {"status": "healthy"}
    
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
