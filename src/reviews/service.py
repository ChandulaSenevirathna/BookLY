from src.db.models import Review
from src.auth.service import UserService
from src.books.service import BookService
from src.reviews.schemas import ReviewCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status

class ReviewService:
    
    async def add_review_to_book(self, user_email:str, book_uid:str, review_data:ReviewCreateModel,
                                 session:AsyncSession):
        
        try:
            pass
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Oops something went wrong")