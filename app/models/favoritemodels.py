from pydantic import BaseModel

class favorite(BaseModel):
    user_id: str
    book_id: int
