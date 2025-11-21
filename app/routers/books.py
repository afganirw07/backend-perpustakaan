from fastapi import APIRouter, Depends
from app.db.database import supabase
from app.models.booksmodels import Books
from datetime import datetime
from app.core.security import verify_token

router = APIRouter()

# create new book
@router.post("/books/create", dependencies=[Depends(verify_token)])
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

# read by params
@router.get("/books/{book_id}")
def read_book(book_id: int):
    response = supabase.table("books").select("*").eq("id", book_id).execute()
    return response.data

# edit book
@router.put("/books/{book_id}", dependencies=[Depends(verify_token)])
def update_book(book_id: int, book: Books):
    data = book.dict(exclude_unset=True)

    # konversi semua datetime ke string ISO
    for key, value in data.items():
        if isinstance(value, datetime):
            data[key] = value.isoformat()
    
    response = supabase.table("books").update(data).eq("id", book_id).execute()
    return response.data

# delete book
@router.delete("/books/{book_id}", dependencies=[Depends(verify_token)])
def delete_book(book_id: int):
    response = supabase.table("books").delete().eq("id", book_id).execute()
    return response.data
