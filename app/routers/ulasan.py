from fastapi import APIRouter, HTTPException
from app.db.database import supabase
from app.models.ulasanmodels import ReviewCreate
from datetime import datetime
import uuid

router = APIRouter()


@router.post("/review/create")
def create_review(payload: ReviewCreate):
    existing = (
        supabase.table("book_reviews")
        .select("*")
        .eq("borrow_id", str(payload.borrow_id))
        .execute()
    )

    if existing.data:
        raise HTTPException(
            status_code=400,
            detail="Review untuk peminjaman ini sudah dibuat."
        )

    new_id = str(uuid.uuid4())

    data = {
        "id": new_id,
        "borrow_id": str(payload.borrow_id),
        "user_id": str(payload.user_id),
        "book_id": payload.book_id,
        "rating": payload.rating,
        "review_text": payload.review_text,
        "created_at": datetime.utcnow().isoformat()
    }

    result = (
        supabase.table("book_reviews")
        .insert(data)
        .execute()
    )

    return {"success": True, "data": result.data[0]}


@router.get("/review/{borrow_id}")
def get_review_by_borrow(borrow_id: str):
    result = (
        supabase.table("book_reviews")
        .select("*")
        .eq("borrow_id", borrow_id)
        .single()
        .execute()
    )

    if result.data is None:
        raise HTTPException(status_code=404, detail="Review tidak ditemukan.")

    return {"success": True, "data": result.data}


@router.get("/review/book/{book_id}")
def get_reviews_by_book(book_id: int):
    result = (
        supabase.table("book_reviews")
        .select("*, users(full_name)")
        .eq("book_id", book_id)
        .execute()
    )

    return {"success": True, "data": result.data}



@router.get("/review/user/{user_id}")
def get_reviews_by_user(user_id: str):
    result = (
        supabase.table("book_reviews")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )

    return {"success": True, "data": result.data}
