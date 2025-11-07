# app/main.py
from fastapi import FastAPI
from app.routers import books

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Look Ma, I'm deployed!"}

app.include_router(books.router)
