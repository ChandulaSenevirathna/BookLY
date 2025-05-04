from aiohttp import Payload
from passlib.context import CryptContext
from datetime import timedelta, datetime
import jwt
from src.config import config

password_context = CryptContext(
    schemes=['bcrypt']
)

def generate_password_hash(password: str):
    """
    Hash a password using bcrypt.
    """
    return password_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    """
    Verify a plain password against a hashed password.
    """
    return password_context.verify(plain_password, hashed_password)

def create_access_token(user_data: dict, expiry_time: timedelta):
    """
    Create an access token for the user.
    """
    
    Payload = {}
    
    token = jwt.encode(
        payload = Payload,
        key = config.JWT_SECRET_KEY,
        algorithm = config.JWT_ALGORITHM,
    )
    
    return token

