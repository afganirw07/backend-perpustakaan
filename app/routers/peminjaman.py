from fastapi import APIRouter
from app.db.database import supabase
from app.models.peminjamanmodels import BorrowRequest
from datetime import datetime, date
import uuid

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
def update_status(id: str, status: str):
    allowed_status = ["pending", "acc", "ditolak", "dikembalikan"]

    if status not in allowed_status:
        return {"success": False, "message": "Status tidak valid"}

    response = (
        supabase.table("borrow_requests")
        .update({"status": status, "updated_at": datetime.utcnow()})
        .eq("id", id)
        .execute()
    )

    return {
        "success": True,
        "message": f"Status berhasil diubah ke {status}",
        "data": response.data
    }
