from fastapi import APIRouter, Depends, HTTPException
from app.db.database import supabase
from app.models.usersmodels import Users
from datetime import datetime
from app.core.security import verify_token
import uuid

router = APIRouter()

# CREATE USER 
@router.post("/users/create", dependencies=[Depends(verify_token)])
def create_user(user: Users):
    try:
        auth_response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password,
        })
        auth_user = auth_response.user
        if not auth_user:
            raise HTTPException(status_code=400, detail="Gagal membuat user di Supabase Auth")

        data = user.dict(exclude_unset=True)
        data["id"] = str(uuid.uuid4())
        data["auth_id"] = auth_user.id
        data["email"] = auth_user.email
        data["password"] = user.password
        data["role_user"] = user.role_user
        data["created_at"] = datetime.utcnow().isoformat()
        data["updated_at"] = datetime.utcnow().isoformat()

        supabase.table("users").insert(data).execute()

        return {"message": "User created successfully. Please verify your email."}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# LOGIN USER
@router.post("/auth/login")
def login_user(data: dict):
    email = data.get("email")
    password = data.get("password")

    response = supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
    })

    # if none
    if not response.user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "access_token": response.session.access_token,
        "refresh_token": response.session.refresh_token,
        "user": response.user.email,
    }


# READ USERS
@router.get("/users", dependencies=[Depends(verify_token)])
def read_users():
    response = supabase.table("users").select("*").execute()
    return response.data


# UPDATE USER
@router.put("/users/{user_id}", dependencies=[Depends(verify_token)])
def update_user(user_id: uuid.UUID, user: Users):
    data = user.dict(exclude_unset=True)
    for key, value in data.items():
        if isinstance(value, datetime):
            data[key] = value.isoformat()
    response = supabase.table("users").update(data).eq("id", str(user_id)).execute()
    return response.data


# DELETE USER
@router.delete("/users/{user_id}", dependencies=[Depends(verify_token)])
def delete_user(user_id: uuid.UUID):
    response = supabase.table("users").delete().eq("id", str(user_id)).execute()
    return response.data
