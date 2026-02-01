"""
CloudJobHunt API - Main Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from datetime import datetime
import logging
import sys

from app.config import settings

# Import all models FIRST to register them with SQLAlchemy before anything else
from app.models import User, CV, Job, JobMatch, SearchPreferences  # noqa: F401

from app.api import auth, users, jobs, frontend, search
from app.database import init_db

# Configure logging early
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)
print("🔧 Main module loaded, creating app...", file=sys.stderr)


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    
    sys.stderr.write("🔧 CREATING APP - STARTING\n")
    sys.stderr.flush()
    logger.info("🔧 Initializing CloudJobHunt API...")
    
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
    
    # Global middleware to log all requests
    @app.middleware("http")
    async def log_all_requests(request, call_next):
        # FIRST THING - log this immediately with ALL headers
        import sys
        headers_str = "; ".join([f"{k}:{v}" for k, v in request.headers.items()])
        sys.stderr.write(f"🌍 INCOMING REQUEST: {request.method} {request.url.path} from {request.client} | Headers: {headers_str}\n")
        sys.stderr.flush()
        logger.info(f"📨 REQUEST: {request.method} {request.url.path} - Host: {request.headers.get('host', 'unknown')} - Client: {request.client}")
        response = await call_next(request)
        logger.info(f"📤 RESPONSE: {response.status_code} for {request.url.path}")
        return response
    
    # Test endpoints (before routers)
    @app.get("/api/v1/test-public")
    async def test_public():
        """Test endpoint - no auth required"""
        return {
            "message": "This is a public endpoint",
            "status": "ok",
            "timestamp": datetime.now().isoformat()
        }
    
    @app.get("/test-no-prefix")
    async def test_no_prefix():
        """Test endpoint without /api/v1 prefix - to see if prefix causes auth"""
        return {
            "message": "Test without API prefix",
            "status": "ok"
        }
    
    @app.get("/api/v1/test-search")
    async def test_search():
        """Test search endpoint - no auth required"""
        return {
            "query": "test",
            "total_found": 3,
            "jobs": [
                {
                    "title": "Test Job 1",
                    "company": "Test Company",
                    "location": "Paris",
                    "description": "Test description",
                    "url": "https://example.com/job1",
                    "source": "test",
                    "posted_date": datetime.now().isoformat(),
                    "job_type": "CDI",
                    "salary": "40K€ - 50K€",
                    "skills": ["Python", "FastAPI"],
                    "days_ago": 0
                },
                {
                    "title": "Test Job 2",
                    "company": "Another Company",
                    "location": "Lyon",
                    "description": "Test description 2",
                    "url": "https://example.com/job2",
                    "source": "test",
                    "posted_date": datetime.now().isoformat(),
                    "job_type": "CDD",
                    "salary": "35K€ - 45K€",
                    "skills": ["JavaScript", "React"],
                    "days_ago": 1
                }
            ],
            "searched_at": datetime.now().isoformat()
        }
    
    # Health & Ready endpoints (before routers)
    @app.get("/health")
    async def health():
        return {"status": "healthy", "service": "CloudJobHunt API", "timestamp": datetime.now().isoformat()}
    
    @app.get("/ready")
    async def ready():
        """Readiness check"""
        return {"status": "ready"}
    
    # Include routers
    try:
        logger.info("  ✓ Including auth router")
        app.include_router(auth.router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["Authentication"])
        logger.info("  ✓ Including search router")
        app.include_router(search.router, prefix=settings.API_V1_PREFIX, tags=["Search"])
        logger.info("  ✓ Including users router")
        app.include_router(users.router, prefix=settings.API_V1_PREFIX, tags=["Users"])
        logger.info("  ✓ Including jobs router")
        app.include_router(jobs.router, prefix=settings.API_V1_PREFIX, tags=["Jobs"])
        logger.info("  ✓ Including frontend router")
        app.include_router(frontend.router, tags=["Frontend"])
        logger.info("✅ CloudJobHunt API initialized successfully!")
    except Exception as e:
        logger.error(f"❌ Error including routers: {e}")
        import traceback
        logger.error(traceback.format_exc())
    
    # Add custom exception handler for all HTTPExceptions
    from fastapi.exceptions import HTTPException as FastAPIHTTPException
    
    @app.exception_handler(FastAPIHTTPException)
    async def custom_http_exception_handler(request, exc):
        logger.error(f"❌ HTTPException: {exc.status_code} - {exc.detail} - Path: {request.url.path} - Client: {request.client}")
        return {"detail": exc.detail}
    
    # Try to initialize DB tables at startup (safe: prints warning if not available)
    try:
        init_db()
    except Exception:
        pass
    return app


try:
    app = create_app()
except Exception as e:
    sys.stderr.write(f"❌ FATAL ERROR creating app: {e}\n")
    import traceback
    traceback.print_exc(file=sys.stderr)
    raise


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
