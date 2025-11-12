from fastapi import APIRouter
from app.db.database import supabase
from app.models.usersmodels import Users
from datetime import datetime
import uuid

router = APIRouter()

# create new user
@router.post("/users/create")
def create_user(user: Users):
    data = user.dict(exclude_unset=True)
    # konversi semua datetime ke string ISO
    for key, value in data.items():
        if isinstance(value, datetime):
            data[key] = value.isoformat()
    response = supabase.table("users").insert(data).execute()
    return response.data

# read all users
@router.get("/users")
def read_users():
    response = supabase.table("users").select("*").execute()
    return response.data

# edit user
@router.put("/users/{user_id}")
def update_user(user_id: int, user: Users):
    data = user.dict(exclude_unset=True)
    # konversi semua datetime ke string ISO
    for key, value in data.items():
        if isinstance(value, datetime):
            data[key] = value.isoformat()
    response = supabase.table("users").update(data).eq("id", user_id).execute()
    return response.data

# delete user
@router.delete("/users/{user_id}")
def delete_user(user_id: uuid.UUID):
    response = supabase.table("users").delete().eq("id", user_id).execute()
    return response.data