from typing import Optional
from datetime import date
from pydantic import BaseModel
import uuid

class BorrowRequest(BaseModel):
    user_id: uuid.UUID
    book_id: int
    full_name: Optional[str] = ""
    address: Optional[str] = None
    tanggal_peminjaman: Optional[date] = None
    tanggal_pengembalian: Optional[date] = None
    status: Optional[str] = "pending"   
