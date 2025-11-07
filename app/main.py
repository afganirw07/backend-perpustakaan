# app/main.py
from fastapi import FastAPI
from app.routers import books
import os
from dotenv import load_dotenv

# Muat environment variables dari file .env (untuk pengembangan lokal)
load_dotenv()

app = FastAPI(
    title="API Perpustakaan",
    description="API untuk mengelola data buku di perpustakaan.",
    version="1.0.0"
)

# Tambahkan endpoint untuk root URL
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Selamat datang di API Perpustakaan!"}

# Sertakan router buku
app.include_router(books.router, prefix="/api", tags=["Books"])
