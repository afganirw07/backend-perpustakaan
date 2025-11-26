from fastapi import APIRouter, Depends
from app.db.database import supabase
from app.models.booksmodels import Books
from datetime import datetime
from app.core.security import verify_token
# import json
# from app.core.redis import redis_client


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

    # # invalidate cache
    # # redis_client.delete("all_books")

    return response.data

# read all book
@router.get("/books")
def read_books():
    # check cache
    # # cached_books = redis_client.get("all_books")
    # # if cached_books:
    # #     return json.loads(cached_books)

    # if not cached, query db
    response = supabase.table("books").select("*").execute()

    # # set cache
    # # redis_client.set("all_books", json.dumps(response.data), ex=3600) 

    return response.data

# read by params
@router.get("/books/{book_id}")
def read_book(book_id: int):
    # cache_key = f"book:{book_id}"
    # 
    # # check cache
    # # cached_book = redis_client.get(cache_key)
    # # if cached_book:
    # #     return json.loads(cached_book)

    # if not cached, query db
    response = supabase.table("books").select("*").eq("id", book_id).execute()

    # # set cache
    # # if response.data:
        # # redis_client.set(cache_key, json.dumps(response.data), ex=3600) 

    return response.data

# edit book
@router.put("/books/{book_id}", dependencies=[Depends(verify_token)])
def update_book(book_id: int, book: Books):
    data = book.dict(exclude_unset=True)
    # # cache_key = f"book:{book_id}"

    # konversi semua datetime ke string ISO
    for key, value in data.items():
        if isinstance(value, datetime):
            data[key] = value.isoformat()
    
    response = supabase.table("books").update(data).eq("id", book_id).execute()

    # # invalidate cache
    # # redis_client.delete(cache_key)
    # # redis_client.delete("all_books")

    return response.data

# delete book
@router.delete("/books/{book_id}", dependencies=[Depends(verify_token)])
def delete_book(book_id: int):
    # # cache_key = f"book:{book_id}"

    response = supabase.table("books").delete().eq("id", book_id).execute()

    # # invalidate cache
    # # redis_client.delete(cache_key)
    # # redis_client.delete("all_books")

    return response.data
