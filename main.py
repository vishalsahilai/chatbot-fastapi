from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config.settings import settings
from routes.chat import router as chat_router
from routes.health import router as health_router
from routes.order import router as order_router
from database.mongodb import get_db, close_db
from utils.logger import logger

# App Initialization
app = FastAPI(
    title="Sadabahar Restaurant Chatbot",
    description="AI-powered restaurant assistant with RAG, memory, and order management",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(chat_router)
app.include_router(health_router)
app.include_router(order_router)

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(status_code=500, content={"detail": "An unexpected error occurred."})

#startup Event
@app.on_event("startup")
async def on_startup():
    logger.info("Sadabahar Restaurant Chatbot starting up...")
    logger.info(f"Environment: {settings.app_env}")
    get_db()
    logger.info("MongoDB connected.")

#shutdown Event
@app.on_event("shutdown")
async def on_shutdown():
    close_db()
    logger.info("Sadabahar Restaurant Chatbot shutting down.")