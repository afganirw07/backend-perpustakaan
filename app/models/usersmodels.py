from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel
import uuid

class Users(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    # user information
    full_name: Optional[str] = Field(default=None, description="Nama lengkap pengguna")
    email: str = Field(index=True, unique=True, description="Alamat email pengguna")
    password: str = Field(description="Password yang sudah di-hash")
    role_user: str = Field(default="user", description="Peran pengguna (user, petugas, superadmin)")
    
    # metadata sistem
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Tanggal pengguna ditambahkan ke sistem")
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Tanggal terakhir pengguna diupdate")
    