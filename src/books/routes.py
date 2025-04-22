from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from typing import List
from BOOKLY.src.books.book_data import books
from BOOKLY.src.books import schemas


book_router = APIRouter()

@book_router.get("", response_model=List[schemas.Book], status_code=status.HTTP_200_OK)
async def get_books():
    return books

@book_router.post("", status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data: schemas.Book):
    new_book = book_data.model_dump()
    books.append(new_book)
    return new_book

@book_router.get("/{book_id}", status_code=status.HTTP_200_OK)
async def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
        
    raise HTTPException(status_code=404, detail="Book not found")

@book_router.put("/{book_id}")
async def update_book(book_id: int, book_data: schemas.BookUpdateModel):
    for book in books:
        if book["id"] == book_id:
            book.update(book_data.model_dump())
            return {
                "status": "success",
                "record": book
                }
    raise HTTPException(status_code=404, detail="Book not found")

@book_router.patch("/{book_id}")
async def update_book(book_id: int, book_data: schemas.BookUpdateModelV1):
    for book in books:
        if book["id"] == book_id:
            book["title"] = book_data.title
            return {
                "status": "success",
                "record": book
                }
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