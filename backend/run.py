import uvicorn
from app.database import create_tables

if __name__ == "__main__":
    # Create tables before starting the application
    create_tables()
    
    # Start the FastAPI application
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 