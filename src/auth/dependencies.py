from fastapi import HTTPException
from fastapi.security import HTTPBearer

class AccessTokenBearer(HTTPBearer):
    pass