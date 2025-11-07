from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel


class Books(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # information books
    title: str = Field(index=True, description="Judul buku")
    author: str = Field(index=True, description="Nama penulis")
    publisher: Optional[str] = Field(default=None, description="Penerbit buku")
    year: Optional[int] = Field(default=None, description="Tahun terbit")
    isbn: Optional[str] = Field(default=None, unique=True, description="Kode ISBN buku")
    category: Optional[str] = Field(default=None, description="Kategori atau genre buku")
    description: Optional[str] = Field(default=None, description="Deskripsi singkat buku")
    image: Optional[str] = Field(default=None, description="URL gambar sampul buku")
    
    # stock and status
    stock: int = Field(default=0, description="Jumlah stok buku tersedia")
    total_pages: Optional[int] = Field(default=None, description="Jumlah halaman buku")
    language: Optional[str] = Field(default="Indonesia", description="Bahasa buku")
    location_code: Optional[str] = Field(default=None, description="Kode lokasi rak buku di perpustakaan")
    condition: Optional[str] = Field(default="Baik", description="Kondisi buku (Baru, Baik, Rusak, dll)")
    is_available: bool = Field(default=True, description="Status ketersediaan buku")
    
    # metadata sistem
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Tanggal buku ditambahkan ke sistem")
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Tanggal terakhir buku diupdate")
