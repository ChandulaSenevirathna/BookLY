from email.policy import HTTP
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from src.auth.utils import decode_token
from src.db.redis_client import token_in_blocklist
from src.db.main import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.service import UserService


user_service = UserService()

class TokenBearer(HTTPBearer):
    
    def __init__(self, auto_error = True):
        super().__init__(auto_error=auto_error)
    
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)

        token = creds.credentials
        
        is_token_valid = self.token_valid(token)
        print(f"Token valid: {is_token_valid}")
        
        token_data = decode_token(token)
        print(f"Token data: {token_data}")
        
        if is_token_valid == False:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or expired token",
            )
        
        if await token_in_blocklist(token_data["jti"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"error":"Token has been revoked",
                        "resolution":"Please login again"},
            )
        
        self.verify_token_data(token_data)
        
        return token_data  

    def token_valid(self, token: str):

        token_data = decode_token(token)

        if token_data is not None:
            return True
        else:
            return False
        
    def verify_token_data(self, token_data):
        
        raise NotImplementedError("Subclasses must implement this method")

class AccessTokenBearer(TokenBearer):
    
    def verify_token_data(self, token_data):
        
        if token_data is not None and token_data["refresh"] == True:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Refresh token is not allowed provide Access token",
            )
    
        
class RefreshTokenBearer(TokenBearer):
    
    def verify_token_data(self, token_data):
        
        if token_data is not None and token_data["refresh"] == False:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access token is not allowed provide Refresh token",
            )   
            
async def get_current_user(token_data: dict = Depends(AccessTokenBearer()), session: AsyncSession = Depends(get_session)):
    
    user_email = token_data["user_data"]["email"]
    
    user = await user_service.get_user_by_email(user_email, session)
    
    return user