from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config.settings import settings
from routers.chat import router as chat_router
from routers.health import router as health_router 
from utils.logger import logger 

app = FastAPI(
    title="Sadabahar Restaurant Chatbot API",
    description="AI-powered restaurant assistant with hybrid memory",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)
