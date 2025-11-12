from fastapi import Header, HTTPException, status
from app.core.config import SECRET_ACCESS_TOKEN

def verify_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header"
        )

    token = authorization.replace("Bearer ", "").strip()
    if token != SECRET_ACCESS_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
