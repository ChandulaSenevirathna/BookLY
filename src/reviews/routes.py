from fastapi import APIRouter, Depends, HTTPException
from src.db.main import get_session
from src.reviews.service import ReviewService
from src.reviews.schemas import ReviewCreateModel
from src.db.models import User
from src.auth.dependencies import current_user
from sqlalchemy.ext.asyncio import AsyncSession

reviews_router = APIRouter()
review_service = ReviewService()

@reviews_router.post("/book/{book_uid}")
async def add_review_to_books(book_uid: str, review_data: ReviewCreateModel,
                              current_user: User = Depends(current_user),
                              session: AsyncSession = Depends(get_session)):
    
    
    new_review = await review_service.add_review_to_book(
        user_email=current_user.email,
        book_uid=book_uid,
        review_data=review_data,
        session=session
    )
    
    return new_review