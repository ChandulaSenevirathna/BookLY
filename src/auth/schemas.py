from datetime import datetime
import uuid
from pydantic import BaseModel, Field

class UserCreateModel(BaseModel):
    username: str = Field(max_length=10)
    email: str = Field(max_length=50)
    password: str = Field(min_length=6, max_length=12)
    first_name: str
    last_name: str
    
class UserModel(BaseModel):
    uid: uuid.UUID
    username: str = Field(max_length=10)
    email: str = Field(max_length=50)
    password_hash: str = Field(exclude=True)
    first_name: str
    last_name: str
    is_verified: bool
    created_at: datetime 
    updated_at: datetime