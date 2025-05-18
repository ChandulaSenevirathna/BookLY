from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from typing import List
from src.books import schemas, service
from src.db.main import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.dependencies import AccessTokenBearer, RoleChecker


book_router = APIRouter()
book_service = service.BookService()
access_token_bearer = AccessTokenBearer()
role_checker = RoleChecker(["admin", "user"])

@book_router.get("", response_model=List[schemas.Book], status_code=status.HTTP_200_OK)
async def get_books(session: AsyncSession = Depends(get_session), user_details = Depends(AccessTokenBearer()),
                    _: bool = Depends(role_checker)):
    
    books = await book_service.get_all_books(session) 
    return books

@book_router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.Book)
async def create_a_book(book_data: schemas.BookCreateModel, session: AsyncSession = Depends(get_session), 
                        user_details = Depends(AccessTokenBearer()), _: bool = Depends(role_checker)):
    
    # new_book_data = book_data.model_dump()
    new_book = await book_service.create_book(book_data, session)
    return new_book

@book_router.get("/{book_uid}", response_model=schemas.Book, status_code=status.HTTP_200_OK)
async def get_book(book_uid: str, session: AsyncSession = Depends(get_session), 
                   user_details = Depends(AccessTokenBearer()), _: bool = Depends(role_checker)):
    
    book = await book_service.get_book(book_uid, session)
    
    if book:
        return book
    else:  
        raise HTTPException(status_code=404, detail="Book not found")


@book_router.patch("/{book_uid}")
async def update_book(book_uid: str, book_data: schemas.BookUpdateModel, session: AsyncSession = Depends(get_session), 
                      user_details = Depends(AccessTokenBearer()), _: bool = Depends(role_checker)):
 
    updated_book = await book_service.update_book(book_uid, book_data, session)
    
    if updated_book:
        return {
            "status": "success",
            "record": updated_book
        }
    else:
        raise HTTPException(status_code=404, detail="Book not found")


@book_router.delete("/{book_uid}", status_code=status.HTTP_200_OK)
async def delete_book(book_uid: str, session: AsyncSession = Depends(get_session), user_details = Depends(AccessTokenBearer()),
                      _: bool = Depends(role_checker)):
    
    deleted_book = await book_service.delete_book(book_uid, session)
    
    if deleted_book:
        return {
            "status": "success",
            "message": "Book deleted successfully"
        }
    else:
        raise HTTPException(status_code=404, detail="Book not found")