# app/main.py
from fastapi import FastAPI , Request, HTTPException, status
from fastapi.responses import JSONResponse
from app.routers import books, auth
from app.core.config import SECRET_ACCESS_TOKEN

app = FastAPI(
    title="API Perpustakaan",
    description="API untuk mengelola data buku di perpustakaan.",
    version="1.0.0"
)

# middleware
@app.middleware("http")
async def verify_token_middleware(request: Request, call_next):
    public_routes = ["/", "/api/login", "/api/register"]
    if request.url.path not in public_routes:
        token = request.headers.get("Authorization")
        if not token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Missing Authorization token"},
            )

        token_value = token.replace("Bearer ", "")
        if token_value != SECRET_ACCESS_TOKEN:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid token"},
            )

    response = await call_next(request)
    return response

# root
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Selamat datang di API Perpustakaan"}

# route book
app.include_router(books.router, prefix="/api", tags=["Books"])

# route user
app.include_router(auth.router, prefix="/api", tags=["Users"])
