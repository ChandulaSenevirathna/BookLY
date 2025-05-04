from fastapi import APIRouter, Depends, HTTPException,status
from src.auth.schemas import UserCreateModel, UserModel, U
from src.auth.service import UserService
from src.db.main import get_session
from src.auth. utils import create_access_token, decode_token


auth_router = APIRouter()
user_service = UserService()

@auth_router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserModel)
async def create_user_account(user_data: UserCreateModel, session=Depends(get_session)):
    
    email = user_data.email
    
    user_exists = await user_service.user_exists(email=email, session=session)
    
    if user_exists == True:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User already exists")  
    else:
        new_user = await user_service.create_user(user_data=user_data, session=session)
        return new_user
    
@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(login_data: UserCreateModel, session=Depends(get_session)):
    
    email = login_data.email
    password = login_data.password
    
    user = await user_service.authenticate_user(email=email, password=password, session=session)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}