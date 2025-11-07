# index.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Look Ma, I'm deployed!"}

@app.get("/api/database")
def health_check():
    return {"status": "good"}

@app.get("/api/afgan")
def health_check():
    return {"afgan": "ganteng"}

# This is important for Vercel
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)