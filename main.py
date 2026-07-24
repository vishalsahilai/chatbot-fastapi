from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config.settings import settings
from routers.chat import router as chat_router
from routers.health import router as health_router 
from utils.logger import logger 


# App Initialization
app = FastAPI(
    title="Sadabahar Restaurant Chatbot API",
    description="AI-powered restaurant assistant with hybrid memory",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"], #Accept any HTTP method — GET, POST, PUT, DELETE, PATCH, etc.
    allow_headers=["*"] #Accept any request header — Authorization, Content-Type, custom headers, etc.
)

# Routers
app.include_router(chat_router)
app.include_router(health_router)
