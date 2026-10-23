"""
Main FastAPI Application Entrypoint.
Smart Hygiene Risk Prediction System.
"""

import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, CURRENT_DIR)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "database"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "ml", "src"))

from database.db import initialize_database, DB_FILE
from routes import prediction, inspections, facilities, analytics


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure database is initialized on server startup
    if not os.path.exists(DB_FILE):
        print("Database not found. Initializing schema...")
        initialize_database()
    yield


app = FastAPI(
    title="Smart Hygiene Risk Prediction System API",
    description="Production-grade AI/ML system predicting hygiene risk levels and continuous risk scores for food and healthcare facilities.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Enable CORS for full frontend accessibility
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(prediction.router)
app.include_router(inspections.router)
app.include_router(facilities.router)
app.include_router(analytics.router)


@app.get("/api/health", tags=["System Health"])
def health_check():
    """
    Service health probe returning uptime and system status.
    """
    return {
        "status": "healthy",
        "service": "Smart Hygiene Risk Prediction API",
        "version": "1.0.0",
        "database_connected": os.path.exists(DB_FILE),
    }


# Exception Handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        loc = " -> ".join([str(x) for x in err["loc"]])
        errors.append({"field": loc, "message": err["msg"]})
    return JSONResponse(
        status_code=422,
        content={"status": "error", "error_type": "ValidationError", "details": errors},
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"status": "error", "error_type": "InternalServerError", "message": str(exc)},
    )


# Mount Static Frontend
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")
if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
