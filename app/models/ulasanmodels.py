from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class ReviewBase(BaseModel):
    borrow_id: UUID
    user_id: UUID
    book_id: int
    rating: int
    review_text: Optional[str] = None


class ReviewCreate(ReviewBase):
    pass


class ReviewResponse(ReviewBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
