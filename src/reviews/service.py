from src.db.models import Review
from src.auth.service import UserService
from src.books.service import BookService
from src.reviews.schemas import ReviewCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status

book_service = BookService()
user_service = UserService()

class ReviewService:
    
    async def add_review_to_book(self, user_email:str, book_uid:str, review_data:ReviewCreateModel,
                                 session:AsyncSession):
        
        try:
            book = await book_service.get_book(book_uid=book_uid, session=session)
            user = await user_service.get_user(email=user_email, session=session)
            
            new_review = Review(
                rating=review_data.rating,
                review=review_data.review,
                user_uid=user.uid,
                book_uid=book.uid
            )
            
            session.add(new_review)
            await session.commit()
            
            return new_review
            
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Oops something went wrong")