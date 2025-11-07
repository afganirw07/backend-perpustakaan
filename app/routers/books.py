from fastapi import APIRouter
from app.db.database import supabase
from app.models.booksmodels import Books
from datetime import datetime

router = APIRouter()

# create new book
@router.post("/books/create")
def create_book(book: Books):
    data = book.dict(exclude_unset=True)
    
    
    # konversi semua datetime ke string ISO
    for key, value in data.items():
        if isinstance(value, datetime):
            data[key] = value.isoformat()
    
    response = supabase.table("books").insert(data).execute()
    return response.data

# read all book
@router.get("/books")
def read_books():
    response = supabase.table("books").select("*").execute()
    return response.data