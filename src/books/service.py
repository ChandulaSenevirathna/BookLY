from sqlmodel.ext.asyncio import AsyncSession
from src.books.schemas import BookCreateModel, BookUpdateModel
from sqlmodel import select, desc
from src.books.models import Book

class BookService:
    
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.execute(statement)
        return result.all()
    
    async def get_book(self, book_uid: str, session: AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.execute(statement)
        return result.first()
    
    async def create_book(self, book_data: BookCreateModel, session: AsyncSession):
        book_data_dict = book_data.model_dump()
        new_book = Book(**book_data_dict)
        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)
        return new_book
    
    async def update_book(self, update_data: BookUpdateModel, session: AsyncSession):
        
        book_to_update = await self.get_book(update_data.uid, session)
        
        update_data_dict = update_data.model_dump()
        
        for key, value in update_data_dict.items():
            setattr(book_to_update, key, value)
        await session.commit()
        await session.refresh(book_to_update)
        return book_to_update
    
    async def delete_book(self, book_data: BookCreateModel, session: AsyncSession):
        pass