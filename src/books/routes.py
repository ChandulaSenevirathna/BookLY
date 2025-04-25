from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from typing import List
from src.books import schemas, service
from src.db.main import get_session
from sqlmodel.ext.asyncio import AsyncSession



book_router = APIRouter()

book_service = service.BookService()

@book_router.get("", response_model=List[schemas.Book], status_code=status.HTTP_200_OK)
async def get_books(session: AsyncSession = Depends(get_session)):
    
    books = await book_service.get_all_books(session)
    return books

@book_router.post("", status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data: schemas.Book, session: AsyncSession = Depends(get_session)):
    
    new_book_data = book_data.model_dump()
    new_book = await book_service.create_book(new_book_data, session)
    return new_book

@book_router.get("/{book_id}", status_code=status.HTTP_200_OK)
async def get_book(book_uid: int, session: AsyncSession = Depends(get_session)):
    
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

@book_router.patch("/{book_id}")
async def update_book(book_id: int, book_data: schemas.BookUpdateModelV1):
    
    
    
    raise HTTPException(status_code=404, detail="Book not found")

@book_router.delete("/{book_id}", status_code=status.HTTP_200_OK)
async def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {
                "status": "success",
                "record": book
                }
    raise HTTPException(status_code=404, detail="Book not found")