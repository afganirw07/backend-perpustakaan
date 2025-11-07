# index.py
from fastapi import FastAPI
from app.routers import books


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Look Ma, I'm deployed!"}

app.include_router(books.router)


# This is important for Vercel
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)