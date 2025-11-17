from fastapi import APIRouter
from app.db.database import supabase
from app.models.favoritemodels import favorite as FavoriteCreate
from datetime import datetime

router = APIRouter()

@router.post("/favorite/create")
def create_favorite(payload: FavoriteCreate):
    data = {
        "user_id": payload.user_id,
        "book_id": payload.book_id,
        "created_at": datetime.utcnow().isoformat()
    }

    response = supabase.table("favorite").insert(data).execute()
    return response.data


@router.get("/favorite/{user_id}")
def read_favorite(user_id: str):
    response = supabase.table("favorite").select("*").eq("user_id", user_id).execute()
    return response.data

@router.get("/favorite/books/{user_id}")
def get_user_favorites(user_id: str):
    # Ambil semua favorite user
    favs = supabase.table("favorite").select("*").eq("user_id", user_id).execute().data
    
    # Ambil detail buku untuk setiap book_id
    book_ids = [f['book_id'] for f in favs]
    books = supabase.table("books").select("*").in_("id", book_ids).execute().data
    
    return books


@router.delete("/favorite/{favorite_id}")
def delete_favorite(favorite_id: str):
    response = supabase.table("favorite").delete().eq("id", favorite_id).execute()
    return response.data
