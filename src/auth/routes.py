from fastapi import APIRouter, Depends, HTTPException,status
from regex import F
from src.auth.schemas import UserCreateModel, UserModel, UserLoginModel
from src.auth.service import UserService
from src.db.main import get_session
from src.auth import utils
from datetime import timedelta
 
auth_router = APIRouter()
user_service = UserService()

@auth_router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserModel)
async def create_user_account(user_data: UserCreateModel, session=Depends(get_session)):
    
    email = user_data.email
    
    user = await user_service.get_user_by_email(email=email, session=session)
    
    if user is not False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User already exists")  
    else:
        new_user = await user_service.create_user(user_data=user_data, session=session)
        return new_user
    
@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(login_data: UserLoginModel, session=Depends(get_session)):
    
    email = login_data.email
    password = login_data.password
    
    user = await user_service.get_user_by_email(email=email, session=session)
    
    if user is not False:
    
        password_valid = utils.verify_password(password, user.password_hash)
        
        if password_valid:
            
            access_token = utils.create_access_token(
                user_data={
                    'email': user.email,
                    'user_uid': str(user.uid)
                }
            )
            
            refresh_token = utils.create_access_token(
                user_data={
                    'email': user.email,
                    'user_uid': str(user.uid)
                },
                expiry_time=timedelta(days=2),
                refresh=True
            )

            return {"message": "Login successful",
                    "user": user,
                    "access_token": access_token,
                    "refresh_token": refresh_token
                    }
        
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
        
   