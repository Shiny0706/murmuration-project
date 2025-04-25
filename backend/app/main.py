from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import surveys, questions, upload

app = FastAPI(
    title="Survey Data API",
    description="API for accessing and manipulating survey data",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(surveys.router, tags=["surveys"])
app.include_router(questions.router, tags=["questions"])
app.include_router(upload.router, tags=["upload"])

@app.get("/")
async def root():
    return {"message": "Welcome to Survey Data API"} 