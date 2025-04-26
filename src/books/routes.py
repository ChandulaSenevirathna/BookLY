from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from typing import List
from src.books import schemas, service
from src.db.main import get_session
from sqlalchemy.ext.asyncio import AsyncSession



book_router = APIRouter()

book_service = service.BookService()

@book_router.get("", response_model=List[schemas.Book], status_code=status.HTTP_200_OK)
async def get_books(session: AsyncSession = Depends(get_session)):
    
    books = await book_service.get_all_books(session)
    return books

@book_router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.Book)
async def create_a_book(book_data: schemas.BookCreateModel, session: AsyncSession = Depends(get_session)):
    
    # new_book_data = book_data.model_dump()
    new_book = await book_service.create_book(book_data, session)
    return new_book

@book_router.get("/{book_uid}", status_code=status.HTTP_200_OK)
async def get_book(book_uid: str, session: AsyncSession = Depends(get_session)):
    
    book = await book_service.get_book(book_uid, session)
    
    if book:
        return book
    else:  
        raise HTTPException(status_code=404, detail="Book not found")

# @book_router.put("/{book_id}")
# async def update_book(book_id: int, book_data: schemas.BookUpdateModel):
#     for book in books:
#         if book["id"] == book_id:
#             book.update(book_data.model_dump())
#             return {
#                 "status": "success",
#                 "record": book
#                 }
#     raise HTTPException(status_code=404, detail="Book not found")

@book_router.patch("/{book_uid}")
async def update_book(book_uid: str, book_data: schemas.BookUpdateModel, session: AsyncSession = Depends(get_session)):
 
    updated_book = await book_service.update_book(book_uid, book_data, session)
    if updated_book:
        return {
            "status": "success",
            "record": updated_book
        }
    raise HTTPException(status_code=404, detail="Book not found")


@book_router.delete("/{book_uid}", status_code=status.HTTP_200_OK)
async def delete_book(book_uid: int, session: AsyncSession = Depends(get_session)):
    
    deleted_book = await book_service.delete_book(book_uid, session)
    
    if deleted_book:
        return {
            "status": "success",
            "message": "Book deleted successfully"
        }
    else:
        raise HTTPException(status_code=404, detail="Book not found")