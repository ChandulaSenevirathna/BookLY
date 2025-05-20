from re import U
from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.responses import JSONResponse
from regex import F
from tomlkit import date
from src.auth.schemas import UserBooksModel, UserCreateModel, UserModel, UserLoginModel
from src.auth.service import UserService
from src.db.main import get_session
from src.auth import utils
from datetime import timedelta, datetime
from src.auth.dependencies import AccessTokenBearer, RefreshTokenBearer, current_user, current_user_with_books, RoleChecker
from src.db.redis_client import add_jti_to_blocklist
 
auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(["admin", "user"])


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
                    'user_uid': str(user.uid),
                    'role': user.role
                }
            )
            
            refresh_token = utils.create_access_token(
                user_data={
                    'email': user.email,
                    'user_uid': str(user.uid),
                    'role': user.role
                },
                expiry_time=timedelta(days=2),
                refresh=True
            )

            return JSONResponse(
                content={
                    "message": "Login successful",
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'user_data': {
                        'email': user.email,
                        'user_uid': str(user.uid),
                        'role': user.role
                    }
                },
                status_code=status.HTTP_200_OK
            )
        
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    
    print(token_details)
    
    if datetime.fromtimestamp(token_details["exp"]) > datetime.now():
        new_access_token = utils.create_access_token(
            user_data=token_details["user_data"],
        )
    
        return JSONResponse(
            content={
                "message": "New access token generated",
                'access_token': new_access_token,
                'user_data': {
                    'email': token_details["user_data"]["email"],
                    'user_uid': token_details["user_data"]["user_uid"]
                }
            },
            status_code=status.HTTP_200_OK
        )
    
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or Token expired")
            
    
    return {}

@auth_router.get("/logout")
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):
    
    print(token_details)
    
    jti = token_details["jti"]
    await add_jti_to_blocklist(jti)
    return JSONResponse(
        content={
            "message": "Logged out successfully"
        },
        status_code=status.HTTP_200_OK
    )
    
@auth_router.get("/me", response_model=UserModel)
async def get_current_user(current_user: dict = Depends(current_user), _: bool = Depends(role_checker)):
    
    return current_user

@auth_router.get("/me_with_books", response_model=UserBooksModel)
async def get_current_user(current_user: dict = Depends(current_user_with_books), _: bool = Depends(role_checker)):
    
    return current_user