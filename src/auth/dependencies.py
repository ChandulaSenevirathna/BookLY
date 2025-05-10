from email.policy import HTTP
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from src.auth.utils import decode_token

class AccessTokenBearer(HTTPBearer):
    
    def __init__(self, auto_error = True):
        super().__init__(auto_error=auto_error)
    
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        
        # print(creds.scheme, creds.credentials)
        
        token = creds.credentials
        
        is_token_valid = self.token_valid(token)
        print(is_token_valid)
        
        token_data = decode_token(token)
        
        if is_token_valid == False:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or expired token",
            )
        
        if token_data["refresh"] == True:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Refresh token is not allowed",
            )
        
        return token_data

    def token_valid(self, token: str):

        token_data = decode_token(token)

        if token_data is not None:
            return True
        else:
            return False
        