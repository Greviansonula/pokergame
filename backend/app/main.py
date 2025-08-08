from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.db import db_manager
from app.core.config import settings
import os


def create_app() -> FastAPI:
    app = FastAPI(
        title="Poker Game API",
        description="API for Texas Hold'em Poker Game",
        version="1.0.0"
    )
    
    # Add CORS middleware
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[frontend_url, "http://frontend:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API routes
    app.include_router(api_router, prefix="/api/v1")
    
    # Initialize database on startup
    @app.on_event("startup")
    async def startup_event():
        db_manager.init_db()
    
    @app.get("/")
    async def root():
        return {"message": "Poker Game API"}
    
    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}
    
    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    uvicorn.run(app, host=host, port=port)