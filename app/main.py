from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
from app.routes import text
import uvicorn  # Import Uvicorn

load_dotenv()  # Load environment variables from .env file

origins = [
    "http://localhost:3000",
    "https://your-production-url.com",
    "*"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
    return {"message": "Hello from FastAPI in Cloud Run!"}

app.include_router(text.router, prefix="/text", tags=["text"])

if __name__ == "__main__":
    port = int(os.environ["PORT"])
    uvicorn.run(app, host="0.0.0.0", port=port)