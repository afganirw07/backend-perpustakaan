from app.db.database import supabase
from app.models.usersmodels import Users
from datetime import datetime
from app.core.security import verify_token
from fastapi import APIRouter, Depends
import uuid

router = APIRouter()

# user login
@router.get("/users/login")
def login_user(email: str, password: str):
    user = supabase.table("users").select("*").eq("email", email).execute()
    if user and user[0]["password"] == password:
        return {"message": "Login successful"}
    return {"message": "Invalid email or password"}, 401