from fastapi import APIRouter, Depends, HTTPException
from app.db.database import supabase
from app.models.usersmodels import Users
from datetime import datetime
from app.core.security import verify_token
import uuid
import bcrypt
from app.utils.login import send_login_email
from fastapi import BackgroundTasks

router = APIRouter()

# CREATE USER 
@router.post("/users/create")
def create_user(user: Users):
    try:
        auth_response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password,
        })
        auth_user = auth_response.user
        if not auth_user:
            raise HTTPException(status_code=400, detail="Gagal membuat user di Supabase Auth")

        data = {
            "full_name": user.full_name,
            "email": user.email,
            "role_user": user.role_user,
            "password": bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }

        supabase.table("users").insert(data).execute()
        return {"message": "User created successfully. Please verify your email."}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# LOGIN USER
@router.post("/auth/login")
def login_user(data: dict, background_tasks: BackgroundTasks):
    email = data.get("email")
    password = data.get("password")

    # Login Supabase Auth
    response = supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
    })

    if not response.user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Ambil data user dari tabel users
    user_record = supabase.table("users") \
        .select("id, full_name, role_user") \
        .eq("email", email) \
        .single() \
        .execute()

    if not user_record.data:
        raise HTTPException(status_code=404, detail="User tidak ditemukan di tabel users")

    # Kirim email, optional
    background_tasks.add_task(send_login_email, email)

    return {
        "access_token": response.session.access_token,
        "refresh_token": response.session.refresh_token,

        "user_id": user_record.data["id"],     
        "full_name": user_record.data["full_name"],
        "role_user": user_record.data["role_user"],
        "email": email,
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
