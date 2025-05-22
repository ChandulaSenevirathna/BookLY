from fastapi import APIRouter, Depends, HTTPException
from src.reviews.service import ReviewService
from src.reviews.schemas import ReviewCreateModel
from src.db.models import User
from src.auth.dependencies import current_user

reviews_router = APIRouter()
review_service = ReviewService()

@reviews_router.post("/book/{book_uid}")
async def add_review_to_books(book_uid: str, review_data: ReviewCreateModel,
                              current_user: User = Depends(current_user)):
    
    print(current_user)