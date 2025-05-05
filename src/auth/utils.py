from aiohttp import Payload
from passlib.context import CryptContext
from datetime import timedelta, datetime
import jwt
from src.config import config
import uuid
import logging

password_context = CryptContext(
    schemes=['bcrypt']
)

ACCESS_TOKEN_EXPIRY = 3600

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


def create_access_token(user_data: dict, expiry_time: timedelta = None, refresh: bool = False):
    """
    Create an access token for the user.
    """
    
    payload = {}
    
    payload['user_data'] = user_data
    payload['exp'] = datetime.now() + (expiry_time if expiry_time is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload["jti"] = str(uuid.uuid4())
    payload["refresh"] = refresh
    
    token = jwt.encode(
        payload=payload,
        key=config.JWT_SECRET_KEY,
        algorithm=config.JWT_ALGORITHM,
    )
    
    return token


def decode_token(token: str):
    """
    Decode a JWT token.
    """
    try:
        payload = jwt.decode(
            token,
            key=config.JWT_SECRET_KEY,
            algorithms=config.JWT_ALGORITHM,
        )
        return payload
    except jwt.PyJWKError as e:
        logging.exception(e)
        return None