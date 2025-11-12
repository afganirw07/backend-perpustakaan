from app.db.database import supabase
from datetime import datetime
from fastapi import APIRouter, HTTPException
from app.core.security import SECRET_ACCESS_TOKEN

router = APIRouter()

# user login
@router.post("/auth/login")
def login_user(data: dict):
    email = data.get("email")
    password = data.get("password")

    # Ambil user dari supabase
    user = supabase.table("users").select("*").eq("email", email).execute().data
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    # verifikasi password (pastikan sudah di-hash sebelumnya)
    if password != user[0]["password"]:
        raise HTTPException(status_code=400, detail="Password salah")

    # return token buat dipakai di frontend
    return {"token": SECRET_ACCESS_TOKEN, "role": user[0]["role"], "email": email}
