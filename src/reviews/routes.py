import re
from fastapi import APIRouter, Depends, HTTPException
from src.reviews.service import ReviewService
from src.reviews.schemas import ReviewCreateModel

reviews_router = APIRouter()
review_service = ReviewService()

@reviews_router.get("/")
async def get_reviews(review_data: ReviewCreateModel):
    
    pass