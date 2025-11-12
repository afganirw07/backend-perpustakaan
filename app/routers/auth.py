from fastapi import APIRouter, Depends
from app.db.database import supabase
from app.models.usersmodels import Users
from datetime import datetime
from app.core.security import verify_token
import uuid

router = APIRouter()

# create user
@router.post("/users/create", dependencies=[Depends(verify_token)])
def create_user(user: Users):
    data = user.dict(exclude_unset=True)
    for key, value in data.items():
        if isinstance(value, datetime):
            data[key] = value.isoformat()
    response = supabase.table("users").insert(data).execute()
    return response.data

# get all users
@router.get("/users", dependencies=[Depends(verify_token)])
def read_users():
    response = supabase.table("users").select("*").execute()
    return response.data

# edit user
@router.put("/users/{user_id}", dependencies=[Depends(verify_token)])
def update_user(user_id: uuid.UUID, user: Users):
    data = user.dict(exclude_unset=True)
    for key, value in data.items():
        if isinstance(value, datetime):
            data[key] = value.isoformat()
    response = supabase.table("users").update(data).eq("id", str(user_id)).execute()
    return response.data

# delete user
@router.delete("/users/{user_id}", dependencies=[Depends(verify_token)])
def delete_user(user_id: uuid.UUID):
    response = supabase.table("users").delete().eq("id", str(user_id)).execute()
    return response.data
