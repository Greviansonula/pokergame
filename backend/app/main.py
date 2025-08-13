from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.db import db_manager
from app.core.config import settings
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    logger.info("Creating FastAPI application")
    try:
        app = FastAPI(
            title="Poker Game API",
            description="API for Texas Hold'em Poker Game",
            version="1.0.0"
        )
        logger.info("FastAPI application created successfully")
        
        # Add CORS middleware
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        logger.info(f"Configuring CORS with frontend URL: {frontend_url}")
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[frontend_url, "http://frontend:3000"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        logger.info("CORS middleware configured successfully")
        
        # Include API routes
        logger.info("Including API router")
        app.include_router(api_router, prefix="/api/v1")
        logger.info("API router included successfully")
        
        # Initialize database on startup
        @app.on_event("startup")
        async def startup_event():
            logger.info("Application startup event triggered")
            try:
                logger.info("Initializing database")
                db_manager.init_db()
                logger.info("Database initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize database during startup: {e}")
                logger.exception("Database startup error details:")
                raise e
        
        @app.get("/")
        async def root():
            logger.debug("Root endpoint called")
            return {"message": "Poker Game API"}
        
        @app.get("/health")
        async def health_check():
            logger.debug("Health check endpoint called")
            try:
                # Test database connection
                with db_manager.get_cursor() as cursor:
                    cursor.execute("SELECT 1")
                    result = cursor.fetchone()
                    if result:
                        logger.debug("Health check: Database connection successful")
                        return {"status": "healthy", "database": "connected"}
                    else:
                        logger.warning("Health check: Database query returned no result")
                        return {"status": "degraded", "database": "query_failed"}
            except Exception as e:
                logger.error(f"Health check failed: {e}")
                logger.exception("Health check error details:")
                return {"status": "unhealthy", "database": "connection_failed", "error": str(e)}
        
        logger.info("FastAPI application setup completed successfully")
        return app
        
    except Exception as e:
        logger.error(f"Failed to create FastAPI application: {e}")
        logger.exception("Application creation error details:")
        raise e


app = create_app()

if __name__ == "__main__":
    import uvicorn
    try:
        host = os.getenv("API_HOST", "0.0.0.0")
        port = int(os.getenv("API_PORT", "8000"))
        logger.info(f"Starting uvicorn server on {host}:{port}")
        uvicorn.run(app, host=host, port=port)
    except Exception as e:
        logger.error(f"Failed to start uvicorn server: {e}")
        logger.exception("Server startup error details:")
        raise e