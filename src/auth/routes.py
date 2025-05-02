from fastapi import APIRouter, Depends, HTTPException,status
from src.auth.schemas import UserCreateModel
from src.auth.service import UserService
from src.db.main import get_session

auth_router = APIRouter()
user_service = UserService()

@auth_router.post("/signup")
async def create_user_account(user_data: UserCreateModel, session=Depends(get_session)):
    
    email = user_data.email
    
    user_exists = await user_service.user_exists(email=email, session=session)
    
    if user_exists == True:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User already exists")  
    else:
        new_user = await user_service.create_user(user_data=user_data, session=session)
        return {"message": "User created successfully", "user": new_user}