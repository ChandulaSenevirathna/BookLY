from datetime import datetime
import uuid
from pydantic import BaseModel, Field
from typing import Optional, List


class Review(BaseModel):
    uid: uuid.UUID
    rating: int = Field(le=5)
    review: str 
    user_uid: Optional[uuid.UUID]
    book_uid: Optional[uuid.UUID]
    created_at: datetime 
    updated_at: datetime 

class ReviewCreateModel(BaseModel):
    rating: int = Field(le=5)
    review: str