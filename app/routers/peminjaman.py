from fastapi import APIRouter
from app.db.database import supabase
from app.models.peminjamanmodels import BorrowRequest
from datetime import datetime, date
import uuid
from fastapi import Query, BackgroundTasks
from typing import Optional
from app.utils.peminjaman import send_peminjaman_status_email


router = APIRouter()


# create peminjaman
@router.post("/peminjaman/create")
def create_peminjaman(request: BorrowRequest):
    data = request.dict(exclude_unset=True)

    # convert UUID, date, datetime to string
    for key, value in data.items():
        if isinstance(value, uuid.UUID):
            data[key] = str(value)

        if isinstance(value, date):
            data[key] = value.isoformat()

        if isinstance(value, datetime):
            data[key] = value.isoformat()

    if "status" not in data or data["status"] is None:
        data["status"] = "pending"

    response = supabase.table("borrow_requests").insert(data).execute()

    return {
        "success": True,
        "message": "Peminjaman berhasil dibuat",
        "data": response.data
    }


# read peminjaman
@router.get("/peminjaman/{user_id}")
def read_peminjaman(user_id: str):
    response = (
    supabase.table("borrow_requests")
    .select("*, books(title, author, description, image)")
    .eq("user_id", user_id)
    .execute()
)

    return response.data

# read allpeminjaman
@router.get("/peminjaman")
def read_peminjaman():
    response = supabase.table("borrow_requests").select("*, books(title, author, description, image)").execute()
    return response.data



# edit status
@router.put("/peminjaman/status/{id}")
def update_status(id: str, status: str, background_tasks: BackgroundTasks, alasan: Optional[str] = Query(None, description="Alasan penolakan jika status 'ditolak'")):
    allowed_status = ["pending", "disetuju", "ditolak", "dikembalikan"]

    if status not in allowed_status:
        return {"success": False, "message": "Status tidak valid"}

    update_data = {"status": status, "updated_at": datetime.utcnow().isoformat()}    
    if status == "ditolak":
        update_data["alasan"] = alasan

    response = (
        supabase.table("borrow_requests")
        .update(update_data)
        .eq("id", id)
        .execute()

    )

    if response.data and (status == "disetuju" or status == "ditolak"):
        user_id = response.data[0].get("user_id")
        if user_id:
            user_record = supabase.table("users").select("email").eq("id", user_id).single().execute()
            if user_record.data:
                receiver_email = user_record.data.get("email")
                if status == "disetuju":
                    background_tasks.add_task(
                        send_peminjaman_status_email,
                        receiver_email=receiver_email,
                        status=status
                    )
                elif status == "ditolak":
                    background_tasks.add_task(
                        send_peminjaman_status_email,
                        receiver_email=receiver_email,
                        status=status,
                        alasan=alasan
                    )


    return {
        "success": True,
        "message": f"Status berhasil diubah ke {status}",
        "data": response.data
    }
