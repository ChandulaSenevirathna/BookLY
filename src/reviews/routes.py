import re
from fastapi import APIRouter, Depends, HTTPException


reviews_router = APIRouter()

@reviews_router.get("/")
async def get_reviews():
    """
    Get all reviews.
    """
    return {"message": "Get all reviews"}