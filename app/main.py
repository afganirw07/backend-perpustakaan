# app/main.py
from fastapi import FastAPI
from app.routers import books, auth
from app.service.auth import login_user
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# cors settings
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    return {"message": "Selamat datang di API Perpustakaan"}

# route book
app.include_router(books.router, prefix="/api", tags=["Books"])

# route user
app.include_router(auth.router, prefix="/api", tags=["Users"])

# route login
app.include_router(login_user, prefix="/api", tags=["Login"])
