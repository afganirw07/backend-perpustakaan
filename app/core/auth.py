from fastapi import Depends, HTTPException, Header
from app.core.security import verify_token
from app.db.database import supabase


# ambil user dari token
def get_current_user(Authorization: str = Header(None)):
    if Authorization is None:
        raise HTTPException(401, "Token missing")

    token = Authorization.replace("Bearer ", "")

    try:
        payload = verify_token(token)
        email = payload.get("email")

        user = supabase.table("users") \
            .select("id, role_user, full_name, email") \
            .eq("email", email).single().execute()

        if not user.data:
            raise HTTPException(404, "User tidak ditemukan")

        return user.data

    except:
        raise HTTPException(401, "Token invalid")

def allow_roles(*roles):
    def wrapper(current_user = Depends(get_current_user)):
        if current_user["role_user"] not in roles:
            raise HTTPException(403, "Forbidden: Role tidak diizinkan")
        return current_user
    return wrapper
