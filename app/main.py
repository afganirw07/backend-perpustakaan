# app/main.py
from fastapi import FastAPI
from app.routers import books
import os
from dotenv import load_dotenv

# load env
load_dotenv()

app = FastAPI(
    title="API Perpustakaan",
    description="API untuk mengelola data buku di perpustakaan.",
    version="1.0.0"
)

# root
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Selamat datang di API Perpustakaan!"}

# route book
app.include_router(books.router, prefix="/api", tags=["Books"])
